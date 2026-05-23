import csv
import json
import os
import sys
import time
import traceback

import numpy as np
import psutil
import torch
from PIL import Image
from torch.cuda.amp import autocast
from transformers import AutoImageProcessor, AutoModel

MANIFEST_PATH = r"experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts\sample_manifest.csv"
MODEL_ID = "microsoft/rad-dino"
CHECKPOINT_DIR = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
OUTPUT_SUMMARY = r"experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\rad_dino_embedding_summary.json"
OUTPUT_EMBEDDINGS = r"experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\rad_dino_embeddings.npz"

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

DEVICE_PRIMARY = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE_ACTIVE = DEVICE_PRIMARY
OOM_FALLBACK_TRIGGERED = False

def get_weight_source():
    for root, dirs, files in os.walk(CHECKPOINT_DIR):
        for d in dirs:
            if "models--microsoft--rad-dino" in d:
                full = os.path.join(root, d)
                for _root2, _dirs2, _files2 in os.walk(full):
                    if any(f.endswith(".safetensors") for f in _files2):
                        return "local_cache"
    return "downloaded"

def get_gpu_info(device_str):
    if not torch.cuda.is_available():
        return {"cuda_available": False, "gpu_name": None, "vram_total_mb": None, "vram_allocated_mb_after_model_load": None}
    props = torch.cuda.get_device_properties(0)
    return {
        "cuda_available": True,
        "gpu_name": props.name,
        "vram_total_mb": round(props.total_mem / (1024 * 1024), 1),
        "vram_allocated_mb_after_model_load": round(torch.cuda.memory_allocated(0) / (1024 * 1024), 1),
    }

def get_cpu_memory():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "available_gb": round(mem.available / (1024 ** 3), 2),
        "used_percent": mem.percent,
    }

def load_model(device):
    print(f"[INFO] Loading image processor for {MODEL_ID} ...")
    processor = AutoImageProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
    print(f"[INFO] Loading model {MODEL_ID} on {device} ...")
    model = AutoModel.from_pretrained(MODEL_ID, trust_remote_code=True).to(device)
    model.eval()
    return processor, model

def infer_one(model, processor, img_path, device):
    img = Image.open(img_path).convert("RGB")
    inputs = processor(images=img, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        with autocast():
            outputs = model(**inputs)
    emb = outputs.last_hidden_state[:, 0, :].cpu().numpy()
    if device == "cuda":
        torch.cuda.empty_cache()
    return emb

def main():
    global DEVICE_ACTIVE, OOM_FALLBACK_TRIGGERED

    results = {
        "model_id": MODEL_ID,
        "weight_source": None,
        "images_attempted": 0,
        "images_succeeded": 0,
        "images_failed": 0,
        "embedding_shape": None,
        "hidden_size": None,
        "runtime_seconds": None,
        "cpu_memory_observation": None,
        "gpu_vram_observation": None,
        "failure_details": [],
        "medical_claims": "none",
        "first_embedding_preview": [],
        "weights_downloaded_this_session": True,
        "oom_cpu_fallback_triggered": False,
        "effective_device": DEVICE_PRIMARY,
    }

    t0 = time.time()
    results["cpu_memory_observation"] = get_cpu_memory()
    results["weight_source"] = get_weight_source()
    print(f"[INFO] Weight source: {results['weight_source']}")

    processor = None
    model = None

    try:
        processor, model = load_model(DEVICE_PRIMARY)
        results["gpu_vram_observation"] = get_gpu_info(DEVICE_PRIMARY)
    except (torch.cuda.OutOfMemoryError, RuntimeError) as e:
        if "CUDA" in str(e) or "out of memory" in str(e).lower() or DEVICE_PRIMARY == "cpu":
            print(f"[WARN] GPU OOM during model load: {e}")
            print("[INFO] Falling back to CPU ...")
            OOM_FALLBACK_TRIGGERED = True
            DEVICE_ACTIVE = "cpu"
            results["effective_device"] = "cpu"
            if processor is None:
                processor, model = load_model("cpu")
            results["gpu_vram_observation"] = get_gpu_info("cpu")
        else:
            raise

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    results["images_attempted"] = len(rows)
    print(f"[INFO] Processing {len(rows)} images on {DEVICE_ACTIVE} ...")

    all_embeddings = []
    success_indices = []

    for idx, row in enumerate(rows):
        img_path = row["resolved_image_path"]
        sample_idx = row.get("sample_index", str(idx))
        try:
            emb = infer_one(model, processor, img_path, DEVICE_ACTIVE)
            all_embeddings.append(emb)
            success_indices.append(int(sample_idx))
            results["images_succeeded"] += 1
            if idx % 20 == 0:
                print(f"[INFO] Processed {idx + 1}/{len(rows)} images ...")
        except (torch.cuda.OutOfMemoryError, RuntimeError) as oom_e:
            msg = str(oom_e)
            if ("CUDA" in msg or "out of memory" in msg.lower()) and DEVICE_ACTIVE == "cuda":
                print(f"[WARN] GPU OOM at image {sample_idx}. Switching to CPU fallback ...")
                OOM_FALLBACK_TRIGGERED = True
                DEVICE_ACTIVE = "cpu"
                results["effective_device"] = "cpu"
                del model
                torch.cuda.empty_cache()
                processor, model = load_model("cpu")
                try:
                    emb = infer_one(model, processor, img_path, "cpu")
                    all_embeddings.append(emb)
                    success_indices.append(int(sample_idx))
                    results["images_succeeded"] += 1
                    print(f"[INFO] Image {sample_idx} recovered on CPU")
                except Exception as cpu_e:
                    results["images_failed"] += 1
                    results["failure_details"].append({
                        "sample_index": sample_idx,
                        "path": img_path,
                        "error": f"CPU fallback also failed: {cpu_e}",
                    })
                    print(f"[WARN] CPU fallback also failed: {cpu_e}")
            else:
                results["images_failed"] += 1
                results["failure_details"].append({
                    "sample_index": sample_idx,
                    "path": img_path,
                    "error": str(oom_e),
                })
                print(f"[WARN] Failed image {sample_idx}: {oom_e}")
        except Exception as e:
            results["images_failed"] += 1
            results["failure_details"].append({
                "sample_index": sample_idx,
                "path": img_path,
                "error": str(e),
            })
            print(f"[WARN] Failed image {sample_idx}: {img_path} — {e}")

    t1 = time.time()
    results["runtime_seconds"] = round(t1 - t0, 2)
    results["oom_cpu_fallback_triggered"] = OOM_FALLBACK_TRIGGERED

    if all_embeddings:
        stacked = np.vstack(all_embeddings)
        results["embedding_shape"] = list(stacked.shape)
        results["hidden_size"] = int(stacked.shape[1])
        results["first_embedding_preview"] = [round(float(x), 6) for x in stacked[0, :10]]
        os.makedirs(os.path.dirname(OUTPUT_EMBEDDINGS), exist_ok=True)
        np.savez_compressed(OUTPUT_EMBEDDINGS, embeddings=stacked, indices=np.array(success_indices))
        print(f"[INFO] Saved embeddings to {OUTPUT_EMBEDDINGS}")

    if torch.cuda.is_available():
        results["gpu_vram_observation"]["vram_allocated_mb_after_inference"] = (
            round(torch.cuda.memory_allocated(0) / (1024 * 1024), 1)
        )

    os.makedirs(os.path.dirname(OUTPUT_SUMMARY), exist_ok=True)
    with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"[DONE] Runtime: {results['runtime_seconds']}s")
    print(f"[DONE] Images: {results['images_succeeded']}/{results['images_attempted']} succeeded")
    print(f"[DONE] Embedding shape: {results['embedding_shape']}")
    print(f"[DONE] Hidden size: {results['hidden_size']}")
    print(f"[DONE] OOM fallback triggered: {OOM_FALLBACK_TRIGGERED}")
    print(f"[DONE] Effective device: {DEVICE_ACTIVE}")

    return 0 if results["images_succeeded"] > 0 else 1

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)