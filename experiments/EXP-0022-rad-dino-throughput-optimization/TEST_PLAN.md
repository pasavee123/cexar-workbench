# TEST_PLAN.md

## Goal

Find a practical RAD-DINO embedding configuration that improves throughput compared with EXP-0021 while staying reproducible and safe.

## Baseline

EXP-0021 processed 10,000 images in 498.3 seconds on NVIDIA RTX 6000 Ada, roughly 20.1 images/sec, using a mostly single-image pipeline.

## Candidate Settings

DeepSeek should implement a configurable benchmark runner. The default grid should be conservative:

```text
batch_size: 1, 8, 16, 32, 64
num_workers: 0, 2, 4, 8
sample_size: 2000
```

The runner may stop early for a candidate if:

- CUDA OOM occurs.
- image failure count is non-zero.
- throughput is clearly worse than baseline after a warmup period.

## Required Metrics

For each candidate:

- batch_size
- num_workers
- pin_memory
- prefetch_factor
- persistent_workers
- images_attempted
- images_succeeded
- images_failed
- runtime_seconds, measured after warmup as end-to-end batch time including DataLoader fetch plus GPU inference
- measured_images
- images_per_second, computed as measured_images / measured end-to-end runtime
- peak_allocated_vram_mb
- peak_reserved_vram_mb
- cpu_memory_before/after
- median end-to-end batch latency if feasible
- errors

## Required Artifacts

Large artifacts should stay outside git:

```text
/workspace/exp_artifacts/EXP-0022/
  benchmark_runs/
  review_packet/
```

Lightweight output package:

```text
exp0022_review_packet.tar.gz
```

The package should include:

- `benchmark_results.csv`
- `benchmark_results.json`
- `recommended_config.json`
- `RESULT_DRAFT.md`
- `FAILURE_REPORT_DRAFT.md`
- `EXPERIMENT_LOG_AUTO.md`
- `DIFF_SUMMARY_AUTO.md`
- `artifact_manifest.json`

## Stop Conditions

Stop and write failure drafts if:

- GPU is not NVIDIA RTX 6000 Ada Generation.
- CUDA is unavailable.
- `/opt/venv/bin/python` is unavailable.
- `/workspace/chexpert_dataset_raw` is unavailable.
- no candidate processes at least 100 images successfully.
- any script attempts to delete dataset/cache/repo roots.
- any clinical metric or clinical claim appears.
