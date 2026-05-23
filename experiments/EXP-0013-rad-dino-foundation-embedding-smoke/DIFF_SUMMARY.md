# DIFF_SUMMARY.md

## Experiment Outputs

- `.venvs\cexar-foundation/` was created for RAD-DINO dependencies.
- `artifacts/pip_freeze_cexar_foundation.txt` was created.
- `artifacts/run_rad_dino_embedding_smoke.py` was created.
- `artifacts/rad_dino_embedding_summary.json` was created.
- `artifacts/rad_dino_embeddings.npz` was created.
- RAD-DINO weights were downloaded to the local Hugging Face cache after human approval.

## Scope

No production code, manifests, standards, repo_hunt, EXP-0012B artifacts, `.venvs\cexar-baseline`, or global Python were modified according to the experiment log.

## Known Process Issue

`EXPERIMENT_LOG.md` records cleanup/path-fix actions that were not fully registered in `commands.ps1`. This is a lineage gap, not a model-result failure.

## Restoration Note

`RESTORATION_NOTE.md` documents the accidental snapshot spillover and required-doc restoration performed on 2026-05-24.

## Audit Note

This file was restored on 2026-05-24 after Codex found missing EXP-0013 documentation during EXP-0014 preparation.
