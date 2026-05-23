# REVIEW_NOTES_FOR_CODEX.md

## Review Notes

- EXP-0011 used a read-only source dataset at `D:\Dataset_Chexpert\archive`.
- Five validation frontal JPG images were copied into the experiment folder.
- A filename mapping bug was found and fixed before final result generation.
- The output JSON includes CheXpert sample label rows for context, but no metric calculation was performed.
- The next experiment should create a label crosswalk and compute basic per-label sanity metrics on a larger validation subset.

## Remaining Risks

- XRV labels and CheXpert labels are similar but not identical. A formal crosswalk is required before evaluation.
- No thresholds or calibration were applied.
- This run is not a diagnostic validation.
