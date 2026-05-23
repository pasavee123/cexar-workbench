# RESTORATION_NOTE.md

## Status

EXP-0013 documentation was restored on 2026-05-24 after the experiment folder was accidentally polluted with RAD-DINO snapshot files and several required experiment documents were removed or overwritten.

## What Happened

A manual copy/cleanup operation intended to locate or package RAD-DINO Hugging Face cache weights was run while the terminal working directory was inside:

```text
D:\cexar-workbench\experiments\EXP-0013-rad-dino-foundation-embedding-smoke
```

That operation copied RAD-DINO snapshot files into the experiment root and overwrote or removed some experiment documentation files.

## Restored Files

The following experiment documents were restored from available evidence:

- `README.md`
- `TEST_PLAN.md`
- `RUNNER_INSTRUCTIONS.md`
- `RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`

## Evidence Used

The restored documents were reconstructed from:

- `EXPERIMENT_LOG.md`
- `commands.ps1`
- `artifacts/rad_dino_embedding_summary.json`
- `artifacts/rad_dino_embeddings.npz`
- the prior Codex review of EXP-0013

## Important Boundary

The restored files are audit backfill documents, not original runner-authored files.

They are marked as restored documentation where appropriate.

No model artifact was regenerated. No model was rerun. No production code was modified.

## Remaining Contamination

Some RAD-DINO snapshot files may still exist in the EXP-0013 experiment root, including files such as:

- `config.json`
- `preprocessor_config.json`
- `pyproject.toml`
- `training_images.csv`
- `vitb14_cxr.yaml`
- `augmentations.py`
- `LICENSE`

These files were intentionally not deleted during restoration to avoid destructive cleanup without explicit approval.

## Recommended Follow-Up

Before any cleanup:

1. Create a cleanup plan.
2. List every file proposed for removal.
3. Register cleanup commands in `commands.ps1`.
4. Get human approval.
5. Prefer moving suspected snapshot spillover files into a quarantine folder rather than deleting them.

EXP-0014 may proceed using the restored EXP-0013 documents and existing artifacts.
