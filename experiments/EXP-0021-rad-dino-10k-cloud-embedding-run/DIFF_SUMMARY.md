# DIFF_SUMMARY.md

## Initial Scaffold

- Added EXP-0021 plan for RAD-DINO 10k cloud embedding run.
- Added config and placeholder scripts.
- No production code changed.

## Phase A Script Authoring

- `scripts/build_manifest_10k.py`: deterministic manifest builder.
- `scripts/run_rad_dino_embedding_10k.py`: resumable RAD-DINO embedding extraction.
- `scripts/run_exp0021_10k.sh`: one-shot orchestrator.

## Codex Pre-Run Review Fixes

- Isolated dry-run and full-run artifact roots under `/workspace/exp_artifacts/EXP-0021/runs/<run_label>`.
- Changed embedding extraction to match EXP-0020 by using `last_hidden_state[:, 0, :]`.
- Added strict non-zero exit for partial image failures unless `--allow-partial` is explicitly passed.
- Added failure JSONL output for per-image errors.
- Changed checkpoint semantics so failed images remain retryable on resume.
- Cleaned non-ASCII dash characters from generated documentation.

## Production Code

No production code changed.
