# RESULT.md

## Status

**PASS AS TRUE LINEAR PROBE TRAINING V1**

## Summary

EXP-0017 successfully executed the first controlled downstream linear-probe training experiment for RAD-DINO in CeXaR. All 1,000 images were embedded, all 11 CheXpert labels were probed, and research pipeline metrics were computed with honest per-label masking.

RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE

## Key Findings

### Split Correction
- The corrected patient-level split (seed 42, 70/15/15) is significantly improved over the EXP-0016 random split.
- **Before correction (EXP-0016):** 5 labels required masking (Atelectasis, Pneumonia, Lung Lesion, Fracture, Lung Opacity).
- **After correction (EXP-0017):** Only 1 label requires partial masking (Fracture, val_positive=1).
- The 4 previously problematic labels (Atelectasis, Pneumonia, Lung Lesion, Lung Opacity) are now fully trainable with this split seed.

### Embedding Pipeline
- 1000/1000 images (100.0%) successfully embedded.
- Runtime: 1161.52 seconds (~19.4 minutes) on CPU (i7-12700H).
- Throughput: 0.86 images/second on CPU.
- Embedding dimension: 768 (RAD-DINO CLS token).
- Pipeline is demonstrably reproducible and scalable on CPU.

### Probe Training
- All 11 LogisticRegression probes trained successfully (class_weight=balanced, max_iter=1000, solver=lbfgs).
- **Train AUROC: 1.0 on all labels.** This indicates perfect separation on training data and is consistent with severe overfitting: 768 frozen embedding features for ~700 training samples with no regularization beyond balanced class weights. This is expected behavior for this experimental setup and should not be interpreted as meaningful performance.
- Test AUROC ranges from 0.4360 (Consolidation) to 0.7887 (Pneumothorax).
- Pleural Effusion shows the most consistent train/val/test behavior (test: 0.6992, val: 0.6956).

### Per-Label Test Metrics

RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE

| Label | Train Pos/Neg | Val Pos/Neg | Test Pos/Neg | Val AUROC | Test AUROC | Val AUPRC | Test AUPRC |
|-------|--------------|-------------|--------------|-----------|------------|-----------|------------|
| Atelectasis | 105/593 | 28/124 | 30/120 | 0.4202 | 0.5139 | 0.1806 | 0.2042 |
| Consolidation | 44/654 | 11/141 | 12/138 | 0.6267 | 0.4360 | 0.1380 | 0.1068 |
| Pneumothorax | 67/631 | 12/140 | 16/134 | 0.7339 | 0.7887 | 0.1534 | 0.4451 |
| Edema | 180/518 | 46/106 | 40/110 | 0.7406 | 0.6875 | 0.5143 | 0.4268 |
| Pleural Effusion | 255/443 | 68/84 | 65/85 | 0.6956 | 0.6992 | 0.6912 | 0.6578 |
| Pneumonia | 22/676 | 6/146 | 4/146 | 0.8002 | 0.6747 | 0.1792 | 0.0540 |
| Cardiomegaly | 85/613 | 25/127 | 23/127 | 0.7877 | 0.6806 | 0.4490 | 0.3113 |
| Lung Lesion | 32/666 | 6/146 | 6/144 | 0.6952 | 0.6528 | 0.0710 | 0.0904 |
| Fracture | 32/666 | 1/151* | 4/146 | MASKED | 0.5651 | MASKED | 0.0556 |
| Lung Opacity | 339/359 | 64/88 | 80/70 | 0.6278 | 0.6614 | 0.5314 | 0.7124 |
| Enlarged Cardiomediastinum | 36/662 | 10/142 | 9/141 | 0.3979 | 0.6438 | 0.0562 | 0.1104 |

*Fracture validation metrics masked: validation_positive=1 (below minimum threshold of 3).

## Pass Criteria Evaluation

| Criterion | Status |
|-----------|--------|
| Input manifest valid (1000 rows, 11 labels) | PASS |
| Corrected patient-level split produced | PASS |
| Metric masking honestly documented | PASS |
| RAD-DINO embeddings generated for >=95% of images (100.0%) | PASS |
| At least one label trained successfully (11/11) | PASS |
| Metrics computed only for valid labels/splits | PASS |
| All commands exact in commands.ps1 | PASS |
| No production code modified | PASS |
| No prior experiment artifacts modified | PASS |
| No dataset files modified | PASS |
| No clinical claims made | PASS |

## Limitations (Required Disclosures)

- **Severe overfitting:** Train AUROC = 1.0 on all labels. The 768-dimensional frozen embedding features allow perfect separability on ~700 training samples. This means the models have essentially memorized the training set. The test AUROC values are the only informative metrics.
- **N=1,000 is insufficient** for clinical conclusions or generalization claims.
- **CPU-only inference** (no GPU available on this system).
- **No hyperparameter search** or threshold tuning performed.
- **Class imbalance** addressed only via class_weight='balanced'.
- **Fracture label** is partially masked (validation metrics not computable).
- **Dataset shift risk:** CheXpert is a specific hospital dataset; results may not transfer.
- **No external validation** performed.
- **Label noise and uncertain label policy (U-zeros)** may affect metric interpretation.
- **This is a research pipeline experiment only**, not clinical validation.

## Comparison to Prior Experiments

| Metric | EXP-0013 (smoke) | EXP-0016 (readiness) | EXP-0017 (this) |
|--------|-------------------|----------------------|-----------------|
| Images | 100 | 223,414 (checked) | 1,000 |
| Embeddings | 100 | 0 | 1,000 |
| Probes trained | 0 | 0 | 11 |
| Embedding time | 90s | N/A | 1162s |
| Device | CPU | CPU | CPU |

## Decision

EXP-0017 confirms that the RAD-DINO frozen-embedding downstream training path is technically viable on 1,000 CheXpert images. The pipeline produces reasonable test AUROC values for most labels despite severe training overfitting.

**Next step:** EXP-0018 should consider:
1. Adding regularization (C parameter tuning, elastic net)
2. Scaling to 5,000 images
3. Improved stratified split to fix the Fracture label masking
4. Documenting the overfitting as a known characteristic of the high-dimensional frozen embedding approach

RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE
