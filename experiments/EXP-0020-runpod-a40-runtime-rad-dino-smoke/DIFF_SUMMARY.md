# DIFF_SUMMARY.md

## Status

All files created or modified during EXP-0020 execution.

## Files Modified by Runner

| File | Type of Change | Summary |
|------|---------------|---------|
| `commands.ps1` | Updated | Registered 17 commands (CMD-001 through CMD-017) with purpose, working directory, destructive flag, and results. |
| `EXPERIMENT_LOG.md` | Updated | Chronological log of all phases: environment verification, manifest verification, path mapping correction, smoke test execution. |
| `RESULT.md` | Updated | Complete pass/fail evaluation, runtime metrics, medical claims statement, limitations, artifact references. |
| `FAILURE_REPORT.md` | Updated | Four non-blocking incidents documented: path mapping correction, nvcc missing, HF_HOME/TORCH_HOME not pre-set, du timeout. |
| `DIFF_SUMMARY.md` | Updated | This file. |
| `REVIEW_NOTES_FOR_CODEX.md` | Updated | Summary for Codex review. |

## Files Created by Runner

| File | Summary |
|------|---------|
| `artifacts/rad_dino_cloud_smoke_summary.json` | Full run metadata: GPU, memory, timing, embedding shape, image counts. |
| `artifacts/rad_dino_cloud_smoke_embeddings.npz` | 100 × 768 float32 embeddings plus sample indices. |

## External Files Created

| Path | Summary |
|------|---------|
| `/workspace/.cache/huggingface/` | HuggingFace model cache, 339M after RAD-DINO download. |
| `/workspace/.cache/torch/` | Torch cache directory (created, may be empty). |

## Pre-Run Corrections (Codex)

| File | Type of Change | Summary |
|------|---------------|---------|
| `DATA_ASSET_MANIFEST.md` | Corrected | Replaced earlier per-folder dataset size claims with human-confirmed combined usage of approximately 66G. |
| `network_volume_layout.yaml` | Corrected | Marked per-dataset sizes as values to re-measure in pod. |
| `TEST_PLAN.md` | Updated | Added instruction to log exact `du -sh` values before use. |
| `RUNNER_INSTRUCTIONS.md` | Updated | Added required review branch publishing flow and stop conditions for Git auth. |
| `RUNNER_PREFLIGHT_SAFETY_PROMPT.md` | Updated | Added no-main-push and no-token-logging rules. |
| `TEST_PLAN.md` | Updated | Added review branch publication requirement. |
