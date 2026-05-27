#!/usr/bin/env python3
"""EXP-0022: RAD-DINO DataLoader throughput benchmark.

Benchmarks batched inference across a grid of batch sizes and DataLoader worker
counts. Writes machine-readable results as CSV and JSON.

Usage:
    /opt/venv/bin/python scripts/benchmark_rad_dino_dataloader.py \
        --manifest /workspace/exp_artifacts/EXP-0021/runs/full_10k/manifests/candidate_manifest_10k.csv \
        --results-dir /workspace/exp_artifacts/EXP-0022/benchmark_runs \
        --sample-size 2000 \
        --seed 20260527
"""

import argparse
import csv
import gc
import json
import os
import sys
import time
import traceback

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from PIL import Image
from transformers import AutoModel, AutoImageProcessor


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

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


def cpu_memory_mb():
    try:
        import psutil
        return round(psutil.Process().memory_info().rss / (1024 * 1024), 1)
    except Exception:
        return None


def vram_stats_mb():
    if not torch.cuda.is_available():
        return None, None
    allocated = round(torch.cuda.max_memory_allocated() / (1024 * 1024), 1)
    reserved = round(torch.cuda.max_memory_reserved() / (1024 * 1024), 1)
    return allocated, reserved


def reset_vram_stats():
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()


def load_manifest_paths(manifest_csv):
    import pandas as pd
    df = pd.read_csv(manifest_csv)
    if "resolved_path" not in df.columns:
        print("ERROR: manifest missing 'resolved_path' column", file=sys.stderr)
        sys.exit(1)
    return df["resolved_path"].tolist()


def sample_paths(all_paths, sample_size, seed):
    rng = np.random.RandomState(seed)
    if sample_size >= len(all_paths):
        return all_paths
    indices = rng.permutation(len(all_paths))[:sample_size]
    return [all_paths[i] for i in sorted(indices)]


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

class CheXpertImageDataset(Dataset):
    """Dataset that loads and preprocesses images via AutoImageProcessor."""

    def __init__(self, image_paths, processor):
        self.image_paths = image_paths
        self.processor = processor

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        try:
            img = Image.open(path).convert("RGB")
            inputs = self.processor(images=img, return_tensors="pt")
            pixel_values = inputs["pixel_values"].squeeze(0)
        except Exception:
            return None, path, True
        return pixel_values, path, False


def pad_collate(batch):
    """Collate that filters out failed loads and stacks pixel_values."""
    valid = [(pv, path) for pv, path, failed in batch if not failed]
    if len(valid) == 0:
        return None, [], len(batch)
    pixel_values, paths = zip(*valid)
    pixel_values = torch.stack(pixel_values, dim=0)
    return pixel_values, list(paths), len(batch) - len(valid)


# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------

def run_candidate(model, pixel_values_batch, device):
    with torch.no_grad():
        inputs_batch = pixel_values_batch.to(device, non_blocking=False)
        outputs = model(pixel_values=inputs_batch)
        _emb = outputs.last_hidden_state[:, 0, :]
    return _emb.shape


def benchmark_candidate(
    model,
    all_paths,
    processor,
    batch_size,
    num_workers,
    pin_memory,
    prefetch_factor,
    persistent_workers,
    warmup_batches,
    device,
):
    dataset = CheXpertImageDataset(all_paths, processor)
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        prefetch_factor=prefetch_factor if num_workers > 0 else None,
        persistent_workers=persistent_workers and num_workers > 0,
        collate_fn=pad_collate,
        drop_last=False,
    )

    cpu_before = cpu_memory_mb()
    reset_vram_stats()

    images_succeeded = 0
    images_failed = 0
    total_time = 0.0
    batch_count = 0
    batch_latencies = []
    oom = False
    error_message = None

    iterator = iter(loader)

    try:
        for batch_idx, (pixel_values, paths, fail_count) in enumerate(iterator):
            if pixel_values is None:
                images_failed += fail_count
                continue

            batch_start = time.perf_counter()
            try:
                run_candidate(model, pixel_values, device)
            except torch.cuda.OutOfMemoryError as e:
                oom = True
                error_message = f"CUDA OOM at batch {batch_idx}: {e}"
                torch.cuda.empty_cache()
                break
            batch_end = time.perf_counter()

            actual_batch_size = len(paths)
            images_succeeded += actual_batch_size
            images_failed += fail_count

            if batch_idx < warmup_batches:
                batch_count += 1
                continue

            elapsed = batch_end - batch_start
            total_time += elapsed
            batch_latencies.append(elapsed)
            batch_count += 1

    finally:
        del iterator
        del loader
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    cpu_after = cpu_memory_mb()
    alloc_mb, reserved_mb = vram_stats_mb()

    images_per_second = None
    if total_time > 0 and images_succeeded > 0:
        images_per_second = round(images_succeeded / total_time, 2)

    median_latency = None
    if batch_latencies:
        median_latency = round(float(np.median(batch_latencies)), 4)

    return {
        "batch_size": batch_size,
        "num_workers": num_workers,
        "pin_memory": pin_memory,
        "prefetch_factor": prefetch_factor if num_workers > 0 else None,
        "persistent_workers": persistent_workers and num_workers > 0,
        "images_attempted": len(all_paths),
        "images_succeeded": images_succeeded,
        "images_failed": images_failed,
        "runtime_seconds": round(total_time, 2),
        "images_per_second": images_per_second,
        "peak_allocated_vram_mb": alloc_mb,
        "peak_reserved_vram_mb": reserved_mb,
        "cpu_memory_before_mb": cpu_before,
        "cpu_memory_after_mb": cpu_after,
        "median_batch_latency_s": median_latency,
        "oom": oom,
        "error": error_message,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="EXP-0022 RAD-DINO DataLoader throughput benchmark"
    )
    parser.add_argument("--manifest", required=True, help="Path to EXP-0021 manifest CSV")
    parser.add_argument(
        "--results-dir",
        default="/workspace/exp_artifacts/EXP-0022/benchmark_runs",
    )
    parser.add_argument("--sample-size", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260527)
    parser.add_argument("--model-id", default="microsoft/rad-dino")
    parser.add_argument("--hf-cache", default="/workspace/.cache/huggingface")
    parser.add_argument("--torch-cache", default="/workspace/.cache/torch")
    parser.add_argument("--expected-dim", type=int, default=768)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--batch-sizes", type=int, nargs="+", default=[1, 8, 16, 32, 64])
    parser.add_argument("--num-workers", type=int, nargs="+", default=[0, 2, 4, 8])
    parser.add_argument("--pin-memory", action="store_true", default=True)
    parser.add_argument("--prefetch-factor", type=int, default=2)
    parser.add_argument("--persistent-workers", action="store_true", default=True)
    parser.add_argument("--warmup-batches", type=int, default=2)
    args = parser.parse_args()

    if args.device == "cuda" and not torch.cuda.is_available():
        print("ERROR: CUDA not available but --device is cuda", file=sys.stderr)
        sys.exit(1)

    gpu_name = get_gpu_name()
    print(f"GPU: {gpu_name}")
    print(f"Device: {args.device}")

    os.makedirs(args.results_dir, exist_ok=True)

    print(f"Loading manifest: {args.manifest}")
    all_paths = load_manifest_paths(args.manifest)
    print(f"Total images in manifest: {len(all_paths)}")

    sample_paths_list = sample_paths(all_paths, args.sample_size, args.seed)
    print(f"Sampled {len(sample_paths_list)} images (seed={args.seed})")

    if args.hf_cache:
        os.environ["HF_HOME"] = args.hf_cache
    if args.torch_cache:
        os.environ["TORCH_HOME"] = args.torch_cache

    print(f"Loading processor: {args.model_id} ...")
    processor = AutoImageProcessor.from_pretrained(args.model_id, trust_remote_code=True)
    print(f"Loading model: {args.model_id} to {args.device} ...")
    model = AutoModel.from_pretrained(args.model_id, trust_remote_code=True)
    model = model.to(args.device)
    model.eval()

    total_candidates = len(args.batch_sizes) * len(args.num_workers)
    results = []
    candidate_idx = 0

    for bs in args.batch_sizes:
        for nw in args.num_workers:
            candidate_idx += 1
            label = f"bs={bs}, workers={nw}"
            print(f"\n[{candidate_idx}/{total_candidates}] Benchmarking {label} ...")

            try:
                record = benchmark_candidate(
                    model=model,
                    all_paths=sample_paths_list,
                    processor=processor,
                    batch_size=bs,
                    num_workers=nw,
                    pin_memory=args.pin_memory,
                    prefetch_factor=args.prefetch_factor,
                    persistent_workers=args.persistent_workers,
                    warmup_batches=args.warmup_batches,
                    device=args.device,
                )
                results.append(record)

                if record["oom"]:
                    print(f"  OOM at bs={bs}, workers={nw}: {record['error']}")
                else:
                    print(
                        f"  {record['images_succeeded']} images in "
                        f"{record['runtime_seconds']:.1f}s = "
                        f"{record['images_per_second']} img/s, "
                        f"VRAM alloc={record['peak_allocated_vram_mb']}MB, "
                        f"failed={record['images_failed']}"
                    )

                if record["images_succeeded"] < 100:
                    print(
                        f"  WARNING: fewer than 100 images succeeded for {label}. "
                        f"Stopping this candidate early.",
                        file=sys.stderr,
                    )

            except Exception as e:
                print(f"  ERROR benchmarking {label}: {e}", file=sys.stderr)
                results.append({
                    "batch_size": bs,
                    "num_workers": nw,
                    "pin_memory": args.pin_memory,
                    "prefetch_factor": args.prefetch_factor if nw > 0 else None,
                    "persistent_workers": args.persistent_workers and nw > 0,
                    "images_attempted": len(sample_paths_list),
                    "images_succeeded": 0,
                    "images_failed": 0,
                    "runtime_seconds": 0,
                    "images_per_second": None,
                    "peak_allocated_vram_mb": None,
                    "peak_reserved_vram_mb": None,
                    "cpu_memory_before_mb": None,
                    "cpu_memory_after_mb": None,
                    "median_batch_latency_s": None,
                    "oom": False,
                    "error": repr(e),
                })

            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    csv_path = os.path.join(args.results_dir, "benchmark_results.csv")
    json_path = os.path.join(args.results_dir, "benchmark_results.json")

    benchmark_meta = {
        "experiment_id": "EXP-0022",
        "model_id": args.model_id,
        "gpu_name": gpu_name,
        "device": args.device,
        "manifest": os.path.basename(args.manifest),
        "sample_size": args.sample_size,
        "seed": args.seed,
        "batch_sizes": args.batch_sizes,
        "num_workers": args.num_workers,
        "pin_memory": args.pin_memory,
        "prefetch_factor": args.prefetch_factor,
        "persistent_workers": args.persistent_workers,
        "warmup_batches": args.warmup_batches,
        "candidates": results,
    }

    with open(json_path, "w") as f:
        json.dump(benchmark_meta, f, indent=2)
    print(f"\nJSON results written to: {json_path}")

    fieldnames = [
        "batch_size", "num_workers", "pin_memory", "prefetch_factor",
        "persistent_workers", "images_attempted", "images_succeeded",
        "images_failed", "runtime_seconds", "images_per_second",
        "peak_allocated_vram_mb", "peak_reserved_vram_mb",
        "cpu_memory_before_mb", "cpu_memory_after_mb",
        "median_batch_latency_s", "oom", "error",
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
    print(f"CSV results written to: {csv_path}")

    successful = [r for r in results if not r["oom"] and r["images_succeeded"] > 0]
    if not successful:
        print("ERROR: no candidate processed images successfully", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
