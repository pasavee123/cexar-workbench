import argparse
import csv
import json
import os
import time
from pathlib import Path

import numpy as np
import psutil
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModel


def map_path(raw_path: str, windows_prefix: str, cloud_prefix: str) -> Path:
    normalized = raw_path.replace("\\", "/")
    win_norm = windows_prefix.replace("\\", "/").rstrip("/")
    if normalized.lower().startswith(win_norm.lower()):
        suffix = normalized[len(win_norm):].lstrip("/")
        return Path(cloud_prefix) / suffix
    return Path(normalized)


def gpu_report():
    if not torch.cuda.is_available():
        return {"cuda_available": False}
    props = torch.cuda.get_device_properties(0)
    return {
        "cuda_available": True,
        "device_name": props.name,
        "total_vram_mb": round(props.total_memory / (1024 * 1024), 1),
        "allocated_vram_mb": round(torch.cuda.memory_allocated(0) / (1024 * 1024), 1),
        "reserved_vram_mb": round(torch.cuda.memory_reserved(0) / (1024 * 1024), 1),
    }


def memory_report():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "available_gb": round(mem.available / (1024 ** 3), 2),
        "used_percent": mem.percent,
    }


def read_rows(manifest_path, limit, windows_prefix, cloud_prefix):
    rows = []
    with open(manifest_path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw = row.get("resolved_path") or row.get("resolved_image_path")
            if not raw:
                continue
            mapped = map_path(raw, windows_prefix, cloud_prefix)
            row["_mapped_path"] = str(mapped)
            rows.append(row)
            if len(rows) >= limit:
                break
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--windows-prefix", default=r"D:\Dataset_Chexpert")
    parser.add_argument("--cloud-prefix", default="/mnt/chexpert")
    parser.add_argument("--model-id", default="microsoft/rad-dino")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output-summary", required=True)
    parser.add_argument("--output-embeddings", required=True)
    args = parser.parse_args()

    started = time.time()
    result = {
        "experiment_id": "EXP-0020",
        "model_id": args.model_id,
        "medical_claims": "none",
        "metrics_computed": False,
        "training_performed": False,
        "device_required": "cuda",
        "image_count_requested": args.limit,
        "images_attempted": 0,
        "images_succeeded": 0,
        "images_failed": 0,
        "embedding_shape": None,
        "runtime_seconds": None,
        "cpu_memory_before": memory_report(),
        "gpu_before": gpu_report(),
        "gpu_after_model_load": None,
        "gpu_after_inference": None,
        "failures": [],
    }

    if not torch.cuda.is_available():
        result["failures"].append({"stage": "preflight", "error": "CUDA is not available"})
        write_summary(args.output_summary, result)
        raise SystemExit(1)

    gpu_name = torch.cuda.get_device_name(0)
    if "A40" not in gpu_name:
        result["failures"].append({"stage": "preflight", "error": f"Expected NVIDIA A40, got {gpu_name}"})
        write_summary(args.output_summary, result)
        raise SystemExit(1)

    rows = read_rows(args.manifest, args.limit, args.windows_prefix, args.cloud_prefix)
    readable = [row for row in rows if Path(row["_mapped_path"]).is_file()]
    if len(readable) < args.limit:
        missing = [row["_mapped_path"] for row in rows if not Path(row["_mapped_path"]).is_file()][:10]
        result["failures"].append({
            "stage": "manifest_path_check",
            "error": f"Only {len(readable)}/{args.limit} mapped images are readable",
            "missing_examples": missing,
        })
        write_summary(args.output_summary, result)
        raise SystemExit(1)

    processor = AutoImageProcessor.from_pretrained(args.model_id, trust_remote_code=True)
    model = AutoModel.from_pretrained(args.model_id, trust_remote_code=True).to("cuda")
    model.eval()
    result["gpu_after_model_load"] = gpu_report()

    embeddings = []
    indices = []
    for idx, row in enumerate(readable):
        path = row["_mapped_path"]
        result["images_attempted"] += 1
        try:
            image = Image.open(path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")
            inputs = {key: value.to("cuda") for key, value in inputs.items()}
            with torch.inference_mode():
                with torch.autocast(device_type="cuda", dtype=torch.float16):
                    outputs = model(**inputs)
            emb = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
            embeddings.append(emb)
            indices.append(int(row.get("sample_index", idx)))
            result["images_succeeded"] += 1
            if (idx + 1) % 20 == 0:
                print(f"Processed {idx + 1}/{args.limit}")
        except Exception as exc:
            result["images_failed"] += 1
            result["failures"].append({
                "stage": "inference",
                "sample_index": row.get("sample_index", idx),
                "path": path,
                "error": repr(exc),
            })

    if result["images_succeeded"] != args.limit:
        write_summary(args.output_summary, result)
        raise SystemExit(1)

    stacked = np.vstack(embeddings)
    result["embedding_shape"] = list(stacked.shape)
    result["gpu_after_inference"] = gpu_report()
    result["runtime_seconds"] = round(time.time() - started, 2)

    if result["embedding_shape"] != [args.limit, 768]:
        result["failures"].append({
            "stage": "shape_check",
            "error": f"Expected [{args.limit}, 768], got {result['embedding_shape']}",
        })
        write_summary(args.output_summary, result)
        raise SystemExit(1)

    Path(args.output_embeddings).parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output_embeddings, embeddings=stacked, sample_indices=np.array(indices))
    write_summary(args.output_summary, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def write_summary(path, payload):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


if __name__ == "__main__":
    raise SystemExit(main())

