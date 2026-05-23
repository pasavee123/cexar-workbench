# REVIEW_NOTES_FOR_CODEX.md

## Review Checklist

After the runner completes EXP-0014, Codex should verify:

- No new model inference was run unless explicitly approved.
- No training, AUROC, thresholding, or RAD-DINO classification was performed.
- EXP-0012B and EXP-0013 artifacts were read-only.
- Sample alignment was checked correctly.
- XRV was represented as a classifier output contract.
- RAD-DINO was represented as an embedding backbone contract.
- The adapter draft does not imply clinical readiness.
- Cleanup/move/delete commands were not run or were fully registered and approved.

## Expected Decision

EXP-0014 can establish a multi-model adapter contract direction. It cannot establish model performance or production readiness.
