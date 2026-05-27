# CODEX_REVIEW_PLAN.md

## Review Goal

Codex must review the EXP-0021 scripts before any full 10,000-image cloud run.

## Required Checks

- Scripts are confined to `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run`.
- Large artifacts write only to `/workspace/exp_artifacts/EXP-0021`.
- Dataset roots are read-only from the script perspective.
- No script deletes, moves, or overwrites dataset/cache/repo roots.
- No script installs packages or modifies `/opt/venv`.
- Runtime check requires NVIDIA RTX 6000 Ada Generation.
- Python invocation uses `/opt/venv` or an activated `/opt/venv`.
- Path mapping includes `D:\Dataset_Chexpert\archive`.
- Dry-run modes are implemented.
- Resume/checkpoint behavior is implemented and documented.
- Summary JSON includes image counts, runtime, GPU, cache location, shard list, and failures.
- No training, classifier fitting, AUROC/AUPRC, or clinical claims are present.

## Review Verdicts

- `APPROVE_DRY_RUN_ONLY`
- `APPROVE_FULL_10K_RUN`
- `REQUEST_SCRIPT_FIXES`
- `REJECT_AND_REPLAN`

