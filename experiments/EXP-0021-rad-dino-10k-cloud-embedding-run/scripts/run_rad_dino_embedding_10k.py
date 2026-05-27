#!/usr/bin/env python3
"""EXP-0021: RAD-DINO embedding extraction on CheXpert 10k manifest.

Loads microsoft/rad-dino, processes images from a manifest CSV in shards,
and saves float32 embedding arrays as .npz files.

Features:
  - Resumable: checkpoint progress.json tracks completed indices.
  - Sharded: shard IDs are sequential (incremented per flush), not tied to
    original image indices, so resumed runs append new shards safely.
  - Dry-run: --limit restricts the number of images processed.
  - Validation: non-zero exit on zero successful images or shape mismatch.
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import torch
from PIL import Image
from transformers import AutoModel, AutoImageProcessor


def load_manifest(manifest_path):
    import pandas as pd

    df = pd.read_csv(manifest_path)
    if "resolved_path" not in df.columns:
        print("ERROR: manifest missing 'resolved_path' column", file=sys.stderr)
        sys.exit(1)
    return df["resolved_path"].tolist()


def load_model(model_id, device, hf_cache, torch_cache):
    if hf_cache:
        os.environ["HF_HOME"] = hf_cache
    if torch_cache:
        os.environ["TORCH_HOME"] = torch_cache

    print(f"Loading image processor: {model_id} ...")
    processor = AutoImageProcessor.from_pretrained(model_id, trust_remote_code=True)
    print(f"Loading model: {model_id} to {device} ...")
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True)
    model = model.to(device)
    model.eval()
    return model, processor


def get_gpu_name():
    try:
        import subprocess

        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip().split("\n")[0]
    except Exception:
        if torch.cuda.is_available():
            return torch.cuda.get_device_name(0)
        return "UNKNOWN"


def load_checkpoint(checkpoint_path):
    if os.path.isfile(checkpoint_path):
        with open(checkpoint_path, "r") as f:
            return json.load(f)
    return {
        "completed_indices": [],
        "next_shard_id": 0,
        "success_count": 0,
    }


def save_checkpoint(checkpoint_path, state):
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    tmp_path = checkpoint_path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp_path, checkpoint_path)


def preprocess_image(image_path, processor):
    img = Image.open(image_path).convert("RGB")
    return processor(images=img, return_tensors="pt")


@torch.no_grad()
def extract_embedding(model, inputs, device):
    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model(**inputs)
    # Match EXP-0020 behavior: use the CLS token from last_hidden_state.
    embedding = outputs.last_hidden_state[:, 0, :]
    return embedding.cpu().numpy().astype(np.float32)


def flush_shard(output_dir, shard_id, embeddings_list, paths_list):
    emb_stack = np.vstack(embeddings_list).astype(np.float32)
    out_path = os.path.join(output_dir, f"shard_{shard_id:04d}.npz")
    os.makedirs(output_dir, exist_ok=True)
    np.savez_compressed(out_path, embeddings=emb_stack, paths=np.array(paths_list))
    print(f"  Flushed shard_{shard_id:04d}.npz: shape {emb_stack.shape}")


def main():
    parser = argparse.ArgumentParser(description="EXP-0021 RAD-DINO embedding runner")
    parser.add_argument("--manifest", required=True)
    parser.add_argument(
        "--output-dir",
        default="/workspace/exp_artifacts/EXP-0021/embeddings",
    )
    parser.add_argument(
        "--checkpoint-dir",
        default="/workspace/exp_artifacts/EXP-0021/checkpoints",
    )
    parser.add_argument(
        "--summary-dir",
        default="/workspace/exp_artifacts/EXP-0021/summaries",
    )
    parser.add_argument("--shard-size", type=int, default=1000)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--model-id", default="microsoft/rad-dino")
    parser.add_argument("--hf-cache", default="/workspace/.cache/huggingface")
    parser.add_argument("--torch-cache", default="/workspace/.cache/torch")
    parser.add_argument("--expected-dim", type=int, default=768)
    parser.add_argument("--device", default="cuda")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Allow non-zero image failures. Default is strict: any failed image exits non-zero.",
    )
    args = parser.parse_args()

    if args.device == "cuda" and not torch.cuda.is_available():
        print("ERROR: CUDA not available but --device is cuda", file=sys.stderr)
        sys.exit(1)

    start_time = time.time()
    gpu_name = get_gpu_name()
    print(f"Device: {args.device} ({gpu_name})")

    print(f"Loading manifest: {args.manifest}")
    all_paths = load_manifest(args.manifest)
    total_in_manifest = len(all_paths)
    print(f"Total images in manifest: {total_in_manifest}")

    if args.limit is not None:
        all_paths = all_paths[: args.limit]
        print(f"DRY-RUN: limiting to {len(all_paths)} images (--limit {args.limit})")

    checkpoint_path = os.path.join(args.checkpoint_dir, "progress.json")
    failure_log_path = os.path.join(args.summary_dir, "failures.jsonl")
    state = load_checkpoint(checkpoint_path)

    completed_indices = set(state.get("completed_indices", []))
    success_count = state.get("success_count", 0)
    fail_count = 0
    next_shard_id = state.get("next_shard_id", 0)

    pending_indices = [i for i in range(len(all_paths)) if i not in completed_indices]
    print(
        f"Resume state: {len(completed_indices)} completed, "
        f"{success_count} success, {fail_count} failed, "
        f"{len(pending_indices)} pending, next_shard_id={next_shard_id}"
    )

    model, processor = load_model(args.model_id, args.device, args.hf_cache, args.torch_cache)

    shard_embeddings = []
    shard_paths = []
    processed_this_run = 0
    total_pending = len(pending_indices)
    shape_error_idx = None
    shape_error_shape = None

    for idx in pending_indices:
        img_path = all_paths[idx]

        try:
            inputs = preprocess_image(img_path, processor)
            emb = extract_embedding(model, inputs, args.device)
        except Exception as e:
            print(f"  FAIL [{idx}] {os.path.basename(img_path)}: {e}", file=sys.stderr)
            os.makedirs(args.summary_dir, exist_ok=True)
            with open(failure_log_path, "a", encoding="utf-8") as handle:
                handle.write(json.dumps({
                    "index": idx,
                    "path": img_path,
                    "error": repr(e),
                }) + "\n")
            fail_count += 1
            continue

        if emb.ndim != 2 or emb.shape[1] != args.expected_dim:
            shape_error_idx = idx
            shape_error_shape = emb.shape
            break

        shard_embeddings.append(emb.squeeze(0))
        shard_paths.append(img_path)
        success_count += 1
        completed_indices.add(idx)
        processed_this_run += 1

        if processed_this_run % 100 == 0:
            print(
                f"  Progress: {processed_this_run}/{total_pending} this run, "
                f"success={success_count}, fail={fail_count}"
            )

        if len(shard_embeddings) >= args.shard_size:
            flush_shard(args.output_dir, next_shard_id, shard_embeddings, shard_paths)
            next_shard_id += 1
            shard_embeddings = []
            shard_paths = []
            save_checkpoint(checkpoint_path, {
                "completed_indices": sorted(completed_indices),
                "next_shard_id": next_shard_id,
                "success_count": success_count,
            })

    if shape_error_idx is not None:
        save_checkpoint(checkpoint_path, {
            "completed_indices": sorted(completed_indices),
            "next_shard_id": next_shard_id,
            "success_count": success_count,
        })
        print(
            f"ERROR: embedding shape mismatch at index {shape_error_idx} "
            f"({all_paths[shape_error_idx]}): got {shape_error_shape}, "
            f"expected [1, {args.expected_dim}]",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(shard_embeddings) > 0:
        flush_shard(args.output_dir, next_shard_id, shard_embeddings, shard_paths)
        next_shard_id += 1

    runtime_seconds = time.time() - start_time

    save_checkpoint(checkpoint_path, {
        "completed_indices": sorted(completed_indices),
        "next_shard_id": next_shard_id,
        "success_count": success_count,
    })

    print(f"\nDone. Success: {success_count}, Failed: {fail_count}")
    print(f"Runtime: {runtime_seconds:.1f}s ({runtime_seconds / 60:.1f}m)")

    if success_count == 0:
        print("ERROR: zero successful images", file=sys.stderr)
        sys.exit(1)

    all_files = os.listdir(args.output_dir) if os.path.isdir(args.output_dir) else []
    shard_files = sorted([f for f in all_files if f.startswith("shard_") and f.endswith(".npz")])

    summary = {
        "experiment_id": "EXP-0021",
        "model_id": args.model_id,
        "manifest": os.path.basename(args.manifest),
        "limit": args.limit,
        "total_in_manifest": total_in_manifest,
        "images_attempted": len(completed_indices),
        "images_succeeded": success_count,
        "images_failed": fail_count,
        "embedding_dim": args.expected_dim,
        "shard_size": args.shard_size,
        "num_shards": len(shard_files),
        "shard_files": shard_files,
        "runtime_seconds": round(runtime_seconds, 1),
        "device": args.device,
        "gpu_name": gpu_name,
        "hf_cache": args.hf_cache,
        "torch_cache": args.torch_cache,
        "allow_partial": args.allow_partial,
        "failures_log": failure_log_path if os.path.isfile(failure_log_path) else None,
    }

    os.makedirs(args.summary_dir, exist_ok=True)
    summary_path = os.path.join(args.summary_dir, "exp0021_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary written to: {summary_path}")

    requested_count = len(all_paths)
    if not args.allow_partial and (fail_count > 0 or success_count != requested_count):
        print(
            f"ERROR: strict completion failed. requested={requested_count}, "
            f"success={success_count}, failed={fail_count}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
