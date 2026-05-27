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

Codex verdict: `APPROVE_DRY_RUN_ONLY`.

The next runner may execute dry-run 5 and dry-run 100 only. The full 10k run still requires Codex review of dry-run outputs.
