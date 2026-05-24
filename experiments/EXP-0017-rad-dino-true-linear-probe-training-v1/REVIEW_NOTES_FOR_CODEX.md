# REVIEW_NOTES_FOR_CODEX.md

## Review Checklist

Codex should verify:

- [x] Commands are exact in `commands.ps1`, with no grouped summaries.
- [x] `EXPERIMENT_LOG.md` follows chronological order.
- [x] No package install occurred without approval.
- [x] No network/model download occurred without approval (RAD-DINO weights were locally cached).
- [x] `D:\Dataset_Chexpert` was read-only.
- [x] Prior experiment artifacts (EXP-0013, EXP-0016) were read-only.
- [x] RAD-DINO was frozen and not fine-tuned.
- [x] Corrected split has no patient overlap (verified in Phase 2).
- [x] Metrics are computed only where class representation is valid.
- [x] Metrics are labeled as research pipeline metrics only.
- [x] No clinical claims are made.
- [x] Model artifacts are all inside `artifacts/` and marked experimental.

## Technical Observations for Codex

1. **Overfitting confirmation:** Train AUROC = 1.0 on all 11 labels. This is expected with 768 frozen embedding features for ~700 training samples. The probe has enough capacity to perfectly separate the training data. This means:
   - Test AUROC values are the only informative performance metrics
   - The model has essentially memorized training examples
   - This pattern will appear in all future runs at any sample size unless regularization is added

2. **Split seed sensitivity:** The EXP-0017 corrected split (seed 42) happened to produce a better label distribution than the EXP-0016 split, reducing masked labels from 5 to 1. This was NOT due to stratified correction - the script uses simple random patient-level splitting. The improvement is stochastic. Different random seeds will produce different masking profiles.

3. **Command syntax error (CMD-004):** The initial manifest check used an f-string with escaped backslash quotes, which fails on Python 3.10. This was retried and succeeded. The failed command is logged.

4. **Embedding pipeline throughput:** 0.86 images/second on CPU (i7-12700H). This means:
   - 5,000 images: ~97 minutes
   - Full 223,414 images: ~72 hours on CPU
   - GPU is strongly recommended for any scale-up

5. **Label-level AUROC sanity:** Test AUROC values range from 0.4360 (Consolidation) to 0.7887 (Pneumothorax). While these are above random (0.5), the severe overfitting means these estimates may be unreliable. AUC values near 0.5 may indicate the model is essentially random for those labels.

## Recommendations for EXP-0018

1. Add L2 regularization (lower C value in LogisticRegression) or use RidgeClassifier with CV
2. Scale to 5,000 images
3. Use a fixed stratified patient split to eliminate seed sensitivity
4. Consider dimensionality reduction (PCA on embeddings) as a pre-processing step
5. Run multiple random seeds and report mean/std metrics
6. Compare against an untrained embedding baseline (random linear probe on raw embeddings)

## Expected Decision

EXP-0017 establishes that the RAD-DINO frozen-embedding downstream training path is technically viable on 1,000 CheXpert images. The pipeline executes end-to-end without errors. However, the severe overfitting means that the utility of this approach depends on whether the frozen embeddings contain sufficient signal for the probe to generalize, which is a question for regularization experiments in EXP-0018.

This experiment cannot establish clinical readiness or production readiness.
