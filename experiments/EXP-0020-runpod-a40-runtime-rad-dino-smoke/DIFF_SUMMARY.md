# DIFF_SUMMARY.md

## Status

Not started.

Runner must list every file created or modified during EXP-0020.

## Codex Pre-Run Correction

| File | Type of Change | Summary |
|------|---------------|---------|
| `DATA_ASSET_MANIFEST.md` | Corrected | Replaced earlier per-folder dataset size claims with human-confirmed combined usage of approximately 66G. |
| `network_volume_layout.yaml` | Corrected | Marked per-dataset sizes as values to re-measure in pod. |
| `TEST_PLAN.md` | Updated | Added instruction to log exact `du -sh` values before use. |

## Codex Review Branch Publishing Update

| File | Type of Change | Summary |
|------|---------------|---------|
| `RUNNER_INSTRUCTIONS.md` | Updated | Added required review branch publishing flow and stop conditions for Git auth. |
| `RUNNER_PREFLIGHT_SAFETY_PROMPT.md` | Updated | Added no-main-push and no-token-logging rules. |
| `TEST_PLAN.md` | Updated | Added review branch publication requirement. |
