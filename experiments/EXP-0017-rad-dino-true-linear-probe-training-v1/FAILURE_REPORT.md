# FAILURE_REPORT.md

## Status

No failure recorded. EXP-0017 completed successfully (PASS AS TRUE LINEAR PROBE TRAINING V1).

No stop conditions were triggered. All phases completed without errors.

## Issues Observed (Non-Blocking)

1. **CMD-004 syntax error (retried successfully):** The initial manifest row count command used an f-string with a backslash-escaped quote, which is unsupported in Python 3.10. The command was retried with corrected syntax and succeeded.

2. **Train AUROC = 1.0 on all labels:** This indicates severe overfitting (768 features for ~700 training samples). This is expected for this experimental setup and does not indicate a pipeline failure. It is documented as a limitation in RESULT.md.

3. **Fracture label partially masked:** Validation positive count = 1 (below threshold 3). Validation AUROC/AUPRC are masked for Fracture. Test metrics are computed (test_positive=4, test_negative=146). This is a dataset split limitation, not a pipeline failure.

4. **Only 1 of 5 previously problematic labels remains masked:** The EXP-0016 random split had 5 masked labels. The EXP-0017 corrected split reduced this to 1 (Fracture). The improvement is due to the seed 42 split producing better label distribution than the prior run's split, not due to stratified correction. Different random seeds will produce different split quality.

## Recommended Follow-Up

- None required for EXP-0017. Proceed to EXP-0018 for regularization experiments and scale-up.
