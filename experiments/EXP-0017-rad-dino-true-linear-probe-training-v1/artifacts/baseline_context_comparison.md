# Baseline Context Comparison

**RESEARCH PIPELINE CONTEXT ONLY - NOT CLINICAL PERFORMANCE**

## Scope

EXP-0017 is the first true downstream linear-probe training on 1,000 CheXpert images using frozen RAD-DINO embeddings. It extends the EXP-0013 smoke test (which generated embeddings without training) and EXP-0016 scale-up readiness check (which validated the dataset structure without training).

## Sample Size Comparison

| Experiment | Images | Labels | Training |
|------------|--------|--------|----------|
| EXP-0013 (smoke) | 100 | 0 (embedding only) | None |
| EXP-0016 (readiness) | 223,414 train | 11 labels analyzed | None |
| EXP-0017 (this) | 698 train / 152 val / 150 test | 11 probes trained | LogisticRegression |

## Label Coverage

- Fully trainable labels (all splits have both classes): 10
- Partially masked labels: 1
  - Fracture: ['validation_positive=1']

## Pipeline Readiness

- Input manifest validated.
- Patient-level split created, no patient overlap.
- RAD-DINO frozen embeddings generated.
- Binary LogisticRegression probes trained per label.
- U-zeros uncertain label policy applied.

## Research Pipeline Metrics Summary

| Label | Train AUROC | Val AUROC | Test AUROC | Status |
|-------|-------------|-----------|------------|--------|
| Atelectasis | 1.0 | 0.4202 | 0.5139 | OK |
| Consolidation | 1.0 | 0.6267 | 0.436 | OK |
| Pneumothorax | 1.0 | 0.7339 | 0.7887 | OK |
| Edema | 1.0 | 0.7406 | 0.6875 | OK |
| Pleural Effusion | 1.0 | 0.6956 | 0.6992 | OK |
| Pneumonia | 1.0 | 0.8002 | 0.6747 | OK |
| Cardiomegaly | 1.0 | 0.7877 | 0.6806 | OK |
| Lung Lesion | 1.0 | 0.6952 | 0.6528 | OK |
| Fracture | 1.0 | None | 0.5651 | masked |
| Lung Opacity | 1.0 | 0.6278 | 0.6614 | OK |
| Enlarged Cardiomediastinum | 1.0 | 0.3979 | 0.6438 | OK |

## Limitations

- N=1,000 is insufficient for clinical conclusions.
- CPU-only inference (no GPU).
- No hyperparameter search or threshold tuning.
- Class imbalance not corrected beyond class_weight=balanced.
- 1 of 11 labels requires partial metric masking in EXP-0017: Fracture validation metrics are masked because validation_positive=1. EXP-0016 had 5 labels requiring split correction before this run.
- This is a research pipeline experiment only.

## Comparison to EXP-0013

EXP-0013 generated 100 RAD-DINO embeddings in ~90 seconds on the same hardware. EXP-0017 scales this to 1,000 images and adds downstream training. The embedding pipeline is confirmed to be reproducible and scalable on CPU.

**RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE**
