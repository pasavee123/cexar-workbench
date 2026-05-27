# EXPERIMENT_LOG.md

## 2026-05-27 09:20 UTC - Phase A Start: Script Authoring

- Read all required standards and experiment documentation.
- Reviewed EXP-0020 smoke test reference.
- Reviewed EXP-0016 manifest generation patterns.
- Confirmed three placeholder scripts existed in `scripts/`.

## Phase A Script Implementation

All three scripts were implemented during Phase A:

1. `scripts/build_manifest_10k.py`
   - Reads `train.csv` and `valid.csv` from `/workspace/chexpert_dataset_raw`.
   - Resolves CSV paths by stripping `CheXpert-v1.0-small/` and prepending the dataset root.
   - Validates file existence before inclusion.
   - Prefers frontal images and falls back to non-frontal images if needed.
   - Uses deterministic sampling with seed `20260527`.

2. `scripts/run_rad_dino_embedding_10k.py`
   - Loads `microsoft/rad-dino` through Hugging Face Transformers.
   - Uses checkpointed, sharded embedding extraction.
   - Saves `.npz` shards outside git under `/workspace/exp_artifacts/EXP-0021`.
   - Writes summary JSON and optional failure JSONL.

3. `scripts/run_exp0021_10k.sh`
   - Verifies RTX 6000 Ada, CUDA, `/opt/venv`, `/workspace`, and dataset presence.
   - Builds the deterministic manifest.
   - Runs embedding extraction.
   - Copies lightweight summaries into the git-tracked experiment folder.

No terminal commands were executed on the RunPod instance during Phase A. This was script authoring only.

## 2026-05-27 - Codex Pre-Run Review Fixes

Codex reviewed the Phase A scripts and applied pre-run fixes before approving any cloud dry-run:

- Isolated dry-run and full-run artifacts under `/workspace/exp_artifacts/EXP-0021/runs/<run_label>` so dry-run checkpoints cannot pollute the full 10k run.
- Changed embedding extraction to match EXP-0020 by using `outputs.last_hidden_state[:, 0, :]`.
- Added strict completion behavior: by default, any failed image or incomplete success count exits non-zero.
- Added per-image failure JSONL logging under the run summary directory.
- Changed checkpoint semantics so only successful image indices are marked complete. Failed images remain retryable on resume.
- Cleaned cross-platform documentation characters to ASCII.

## Current Status

Codex pre-run verdict: `APPROVE_DRY_RUN_ONLY`.

The next runner may execute dry-run 5 and dry-run 100 only. The full 10k run still requires Codex review of dry-run outputs.

## 2026-05-27 - Cloud Dry-Run Evidence Backfill

Codex observed lightweight dry-run summaries in the experiment artifact directory:

- `artifacts/dryrun5/exp0021_summary.json`: 5 attempted, 5 succeeded, 0 failed, embedding dimension 768, GPU `NVIDIA RTX 6000 Ada Generation`.
- `artifacts/dryrun100/exp0021_summary.json`: 100 attempted, 100 succeeded, 0 failed, embedding dimension 768, GPU `NVIDIA RTX 6000 Ada Generation`.

These entries are an audit backfill from generated artifact files. The original command ledger had proposed commands but had not yet been updated with observed results.

## 2026-05-27 - Full 10k Run Evidence Backfill

Codex observed the following full-run artifacts:

- `/workspace/exp_artifacts/EXP-0021/runs/full_10k/summaries/exp0021_summary.json`
- `/workspace/exp_artifacts/EXP-0021/runs/full_10k/checkpoints/progress.json`
- `/workspace/exp_artifacts/EXP-0021/runs/full_10k/embeddings/shard_0000.npz` through `shard_0009.npz`
- `artifacts/full_10k/exp0021_summary.json`
- `artifacts/full_10k/manifest_head_20.csv`

The full-run summary reported 10000 attempted, 10000 succeeded, 0 failed, embedding dimension 768, 10 shards, runtime 498.3 seconds, device `cuda`, GPU `NVIDIA RTX 6000 Ada Generation`, `allow_partial` false, and no failures log.

The checkpoint reported `success_count` 10000, `completed_indices` length 10000, first indices `[0, 1, 2]`, last indices `[9997, 9998, 9999]`, and `next_shard_id` 10.

Codex compared the external full-run summary to `artifacts/full_10k/exp0021_summary.json`; they were byte-identical.

Codex inspected the `.npz` shards with `/opt/venv/bin/python`; ten shard files were present, total embedding rows were 10000, and no shard had an embedding shape outside `[N, 768]`.

No clinical metrics were computed. No AUROC/AUPRC was computed. No production code was modified or integrated.

## 2026-05-27 - Final Codex Review

Codex verdict: `PASS_AS_EMBEDDING_REHEARSAL`.

This verdict is limited to 10,000-image embedding extraction artifact production. It does not approve production integration and does not support clinical claims.
