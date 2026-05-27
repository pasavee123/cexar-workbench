# EXPERIMENT_LOG.md

## 2026-05-27 15:08 UTC — Runner session started

Read all required standards and experiment definition files:
- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/RESULT.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/README.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/TEST_PLAN.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/RUNNER_INSTRUCTIONS.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/configs/exp0022_config.yaml`

## 2026-05-27 15:15 UTC — Reference material gathered

Read EXP-0021 implementation scripts for reference patterns:
- `scripts/run_rad_dino_embedding_10k.py` — model loading, embedding extraction
- `scripts/build_manifest_10k.py` — manifest building
- `scripts/run_exp0021_10k.sh` — orchestrator shell script

Key observations from EXP-0021:
- Model: `microsoft/rad-dino` via `AutoModel.from_pretrained(trust_remote_code=True)`
- ImageProcessor: `AutoImageProcessor.from_pretrained(trust_remote_code=True)`
- Embedding: CLS token from `last_hidden_state[:, 0, :]`, dim 768
- Single-image loop, no batching, no DataLoader
- Runtime: 498.3s for 10k images = ~20.1 img/s baseline

## 2026-05-27 15:20 UTC — IMPLEMENTATION: benchmark_rad_dino_dataloader.py

Created `scripts/benchmark_rad_dino_dataloader.py` (~264 lines).

Design decisions:
- Extends EXP-0021 patterns (same model loading, same embedding extraction)
- Uses PyTorch `Dataset` + `DataLoader` for batched inference
- `CheXpertImageDataset`: loads PIL images in `__getitem__`, applies AutoImageProcessor
- `pad_collate`: custom collate that filters failed loads and stacks pixel_values
- `benchmark_candidate()`: runs one (batch_size, num_workers) combination with timing, VRAM measurement, warmup exclusion
- OOM handling: catches `torch.cuda.OutOfMemoryError`, records OOM, calls `torch.cuda.empty_cache()`, continues
- Uses `time.perf_counter()` for batch timing
- Uses `torch.cuda.max_memory_allocated/reserved()` for VRAM
- Uses `psutil.Process().memory_info().rss` for CPU memory
- Output: `benchmark_results.csv` + `benchmark_results.json`
- Grid: 5 batch sizes × 4 worker counts = 20 candidates
- Sample: 2000 images from EXP-0021 manifest (seed 20260527)
- Warmup: 2 batches excluded from timing
- Configurable via CLI: `--batch-sizes`, `--num-workers`, `--pin-memory`, `--prefetch-factor`, `--persistent-workers`, `--warmup-batches`

## 2026-05-27 15:25 UTC — IMPLEMENTATION: run_exp0022_benchmark.sh

Created `scripts/run_exp0022_benchmark.sh` (~128 lines).

Phases:
1. Runtime Verification: GPU check, CUDA check, Python check, dataset check, manifest check
2. Create Output Directories: benchmark_runs, review_packet under `/workspace/exp_artifacts/EXP-0022/`
3. DataLoader Throughput Benchmark: invokes `benchmark_rad_dino_dataloader.py`
4. Generate Review Packet: invokes `generate_review_packet.py`

## 2026-05-27 15:30 UTC — IMPLEMENTATION: generate_review_packet.py

Created `scripts/generate_review_packet.py` (~254 lines).

Functions:
- `load_benchmark_json()`: reads benchmark_results.json
- `select_best_config()`: picks candidate with highest images_per_second
- `generate_result_draft()`: writes RESULT_DRAFT.md with baseline comparison, speedup, recommended config
- `generate_failure_draft()`: writes FAILURE_REPORT_DRAFT.md listing OOM/error candidates
- `generate_diff_summary()`: writes DIFF_SUMMARY_AUTO.md
- `generate_experiment_log()`: writes EXPERIMENT_LOG_AUTO.md
- `generate_artifact_manifest()`: writes artifact_manifest.json with file sizes and SHA-256
- Creates `exp0022_review_packet.tar.gz` containing all generated + copied files

## 2026-05-27 15:35 UTC — Updated commands.ps1 and EXPERIMENT_LOG.md

Registered all planned execution commands (CMD-004 through CMD-007).
Updated this log with implementation progress.

## Status: SCRIPTS IMPLEMENTED — READY FOR CLOUD DEPLOYMENT

All three scripts are implemented and match the TEST_PLAN.md and RUNNER_INSTRUCTIONS.md specifications.
Awaiting execution on the cloud Pod with NVIDIA RTX 6000 Ada Generation.

## 2026-05-27 15:40 UTC — DIFF_SUMMARY.md updated

Recorded all created files in DIFF_SUMMARY.md. No production code was modified. All changes are confined to the EXP-0022 experiment folder.
