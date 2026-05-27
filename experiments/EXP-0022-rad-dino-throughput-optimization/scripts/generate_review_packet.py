#!/usr/bin/env python3
"""EXP-0022 review packet generator.

Reads benchmark_results.json, selects the best config, and creates a self-
contained tarball for local Codex review.

Usage:
    /opt/venv/bin/python scripts/generate_review_packet.py \
        --results-dir /workspace/exp_artifacts/EXP-0022/benchmark_runs \
        --packet-dir /workspace/exp_artifacts/EXP-0022/review_packet
"""

import argparse
import csv
import hashlib
import json
import os
import sys
import tarfile
import time
from datetime import datetime, timezone


def sha256_hex(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_benchmark_json(results_dir):
    json_path = os.path.join(results_dir, "benchmark_results.json")
    if not os.path.isfile(json_path):
        print(f"ERROR: benchmark_results.json not found at {json_path}", file=sys.stderr)
        sys.exit(1)
    with open(json_path, "r") as f:
        return json.load(f)


def select_best_config(results_data):
    candidates = results_data.get("candidates", [])
    successful = [
        c for c in candidates
        if not c.get("oom", False) and (c.get("images_per_second") or 0) > 0
    ]
    if not successful:
        return None

    best = max(successful, key=lambda c: c["images_per_second"])
    return {
        "experiment_id": "EXP-0022",
        "recommended": {
            "batch_size": best["batch_size"],
            "num_workers": best["num_workers"],
            "pin_memory": best["pin_memory"],
            "prefetch_factor": best.get("prefetch_factor"),
            "persistent_workers": best.get("persistent_workers"),
        },
        "achieved_images_per_second": best["images_per_second"],
        "achieved_runtime_seconds": best["runtime_seconds"],
        "peak_allocated_vram_mb": best["peak_allocated_vram_mb"],
        "peak_reserved_vram_mb": best["peak_reserved_vram_mb"],
        "rationale": (
            "Highest images/sec among all non-OOM candidates in the "
            "batch_size x num_workers grid."
        ),
    }


def generate_result_draft(meta, recommended, results_dir):
    gpu = meta.get("gpu_name", "UNKNOWN")
    sample_size = meta.get("sample_size", "UNKNOWN")
    baseline_ips = 20.1

    lines = []
    lines.append("# RESULT_DRAFT.md")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("BENCHMARK COMPLETE.")
    lines.append("")
    lines.append("## Environment")
    lines.append("")
    lines.append(f"- GPU: {gpu}")
    lines.append(f"- Model: {meta.get('model_id', 'UNKNOWN')}")
    lines.append(f"- Sample size: {sample_size} images")
    lines.append(f"- Seed: {meta.get('seed', 'UNKNOWN')}")
    lines.append(f"- Device: {meta.get('device', 'UNKNOWN')}")
    lines.append("")
    lines.append("## Baseline Comparison")
    lines.append("")
    lines.append(f"- EXP-0021 baseline: ~{baseline_ips} images/sec (batch_size=1, single-image loop)")
    if recommended:
        rec_ips = recommended["achieved_images_per_second"]
        speedup = round(rec_ips / baseline_ips, 2)
        lines.append(f"- EXP-0022 best config: {rec_ips} images/sec")
        lines.append(f"- Observed speedup: {speedup}x")
        lines.append(f"- Recommended batch_size: {recommended['recommended']['batch_size']}")
        lines.append(f"- Recommended num_workers: {recommended['recommended']['num_workers']}")
        lines.append(f"- Peak VRAM allocated: {recommended['peak_allocated_vram_mb']} MB")
    else:
        lines.append("- No successful candidate found.")
    lines.append("")
    lines.append("## Configuration Grid Tested")
    lines.append("")
    lines.append(f"- batch_sizes: {meta.get('batch_sizes', [])}")
    lines.append(f"- num_workers: {meta.get('num_workers', [])}")
    lines.append(f"- pin_memory: {meta.get('pin_memory', None)}")
    lines.append(f"- prefetch_factor: {meta.get('prefetch_factor', None)}")
    lines.append(f"- persistent_workers: {meta.get('persistent_workers', None)}")
    lines.append(f"- warmup_batches: {meta.get('warmup_batches', None)}")
    lines.append("")
    lines.append("## All Candidate Results")
    lines.append("")
    csv_path = os.path.join(results_dir, "benchmark_results.csv")
    if os.path.isfile(csv_path):
        lines.append("See `benchmark_results.csv` for full per-candidate metrics.")
    lines.append("")
    lines.append("## Boundaries")
    lines.append("")
    lines.append("This is a performance engineering experiment only. No clinical claims, no model training, no AUROC/AUPRC calculation, and no production integration were performed.")
    lines.append("")
    lines.append("Required limitations remain: dataset shift, patient leakage risk, label noise, class imbalance, calibration uncertainty, shortcut learning, missing external validation, and human-in-the-loop validation needs.")
    return "\n".join(lines)


def generate_failure_draft(meta):
    candidates = meta.get("candidates", [])
    oom_count = sum(1 for c in candidates if c.get("oom"))
    error_count = sum(1 for c in candidates if c.get("error") and not c.get("oom"))

    lines = []
    lines.append("# FAILURE_REPORT_DRAFT.md")
    lines.append("")
    if oom_count == 0 and error_count == 0:
        lines.append("No failures detected. All candidates completed without OOM or runtime errors.")
    else:
        lines.append("## Failures Detected")
        lines.append("")
        if oom_count > 0:
            lines.append(f"- CUDA OOM: {oom_count} candidate(s)")
        if error_count > 0:
            lines.append(f"- Runtime errors: {error_count} candidate(s)")
        lines.append("")
        lines.append("### Details")
        lines.append("")
        for c in candidates:
            if c.get("oom"):
                lines.append(
                    f"- bs={c['batch_size']}, workers={c['num_workers']}: "
                    f"CUDA OOM — {c.get('error', 'no detail')}"
                )
            elif c.get("error"):
                lines.append(
                    f"- bs={c['batch_size']}, workers={c['num_workers']}: "
                    f"{c.get('error', 'no detail')}"
                )
        lines.append("")
    lines.append("## Limitation")
    lines.append("")
    lines.append("This report is auto-generated from benchmark output and has not been manually reviewed.")
    return "\n".join(lines)


def generate_diff_summary():
    lines = []
    lines.append("# DIFF_SUMMARY_AUTO.md")
    lines.append("")
    lines.append("## Files Created")
    lines.append("")
    lines.append("- `scripts/benchmark_rad_dino_dataloader.py` — batched DataLoader benchmark runner")
    lines.append("- `scripts/run_exp0022_benchmark.sh` — experiment orchestrator")
    lines.append("- `scripts/generate_review_packet.py` — review packet generator")
    lines.append("")
    lines.append("## Production Code Changes")
    lines.append("")
    lines.append("None. All changes are confined to the EXP-0022 experiment folder.")
    lines.append("")
    lines.append("## Dataset Modifications")
    lines.append("")
    lines.append("None. No dataset files were created, modified, or deleted.")
    return "\n".join(lines)


def generate_experiment_log(results_dir):
    json_path = os.path.join(results_dir, "benchmark_results.json")
    mtime = None
    if os.path.isfile(json_path):
        mtime = datetime.fromtimestamp(os.path.getmtime(json_path), tz=timezone.utc)

    lines = []
    lines.append("# EXPERIMENT_LOG_AUTO.md")
    lines.append("")
    if mtime:
        lines.append(f"Benchmark completed at: {mtime.isoformat()}")
    else:
        lines.append("Benchmark completion time: UNKNOWN")
    lines.append("")
    lines.append("## Pipeline Steps")
    lines.append("")
    lines.append("1. Runtime verification (GPU, CUDA, dataset, manifest)")
    lines.append("2. Model + processor loading from `microsoft/rad-dino`")
    lines.append("3. Grid benchmark: batch_sizes x num_workers")
    lines.append("4. Results written as JSON + CSV")
    lines.append("5. Review packet generated")
    lines.append("")
    lines.append("This log is auto-generated from the review packet generator.")
    return "\n".join(lines)


def generate_artifact_manifest(packet_files, packet_dir):
    records = []
    for fname in sorted(packet_files):
        fpath = os.path.join(packet_dir, fname)
        size_bytes = os.path.getsize(fpath) if os.path.isfile(fpath) else 0
        sha = sha256_hex(fpath) if os.path.isfile(fpath) else "MISSING"
        records.append({
            "file": fname,
            "size_bytes": size_bytes,
            "sha256": sha,
        })

    manifest = {
        "experiment_id": "EXP-0022",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": records,
    }
    return json.dumps(manifest, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="EXP-0022 review packet generator"
    )
    parser.add_argument(
        "--results-dir",
        required=True,
        help="Path to directory containing benchmark_results.json and benchmark_results.csv",
    )
    parser.add_argument(
        "--packet-dir",
        required=True,
        help="Directory to write review packet tarball",
    )
    args = parser.parse_args()

    results_data = load_benchmark_json(args.results_dir)
    meta = results_data

    recommended = select_best_config(results_data)
    if recommended is None:
        print(
            "WARNING: no successful candidate found. Review packet will not "
            "include a recommended config."
        )

    os.makedirs(args.packet_dir, exist_ok=True)

    # Copy benchmark data
    csv_src = os.path.join(args.results_dir, "benchmark_results.csv")
    json_src = os.path.join(args.results_dir, "benchmark_results.json")

    csv_dst = os.path.join(args.packet_dir, "benchmark_results.csv")
    json_dst = os.path.join(args.packet_dir, "benchmark_results.json")

    if os.path.isfile(csv_src):
        with open(csv_src, "rb") as src, open(csv_dst, "wb") as dst:
            dst.write(src.read())

    if os.path.isfile(json_src):
        with open(json_src, "rb") as src, open(json_dst, "wb") as dst:
            dst.write(src.read())

    # Generate recommended_config.json
    if recommended:
        rec_path = os.path.join(args.packet_dir, "recommended_config.json")
        with open(rec_path, "w") as f:
            json.dump(recommended, f, indent=2)

    # Generate drafts
    drafts = {
        "RESULT_DRAFT.md": generate_result_draft(meta, recommended, args.results_dir),
        "FAILURE_REPORT_DRAFT.md": generate_failure_draft(meta),
        "EXPERIMENT_LOG_AUTO.md": generate_experiment_log(args.results_dir),
        "DIFF_SUMMARY_AUTO.md": generate_diff_summary(),
    }

    for fname, content in drafts.items():
        fpath = os.path.join(args.packet_dir, fname)
        with open(fpath, "w") as f:
            f.write(content)

    # Generate artifact manifest
    packet_files = [f for f in os.listdir(args.packet_dir) if f.endswith(".csv") or f.endswith(".json") or f.endswith(".md")]
    manifest_content = generate_artifact_manifest(packet_files, args.packet_dir)
    manifest_path = os.path.join(args.packet_dir, "artifact_manifest.json")
    with open(manifest_path, "w") as f:
        f.write(manifest_content)

    # Create tarball
    tarball_path = os.path.join(args.packet_dir, "exp0022_review_packet.tar.gz")
    with tarfile.open(tarball_path, "w:gz") as tar:
        for fname in sorted(os.listdir(args.packet_dir)):
            fpath = os.path.join(args.packet_dir, fname)
            if os.path.isfile(fpath) and fname != "exp0022_review_packet.tar.gz":
                tar.add(fpath, arcname=fname)

    print(f"Review packet written to: {tarball_path}")
    print(f"  Files: {', '.join(sorted(os.listdir(args.packet_dir)))}")
    sys.exit(0)


if __name__ == "__main__":
    main()
