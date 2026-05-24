# EXP-0017 Readiness Assessment

## Summary

This is a dataset scale-up readiness check only. This assessment does not train any model, run RAD-DINO inference, or make clinical claims.

## Result

**PARTIAL PASS AS SCALE-UP READINESS CHECK**

The local CheXpert dataset is structurally confirmed for downstream scale-up training. However, the current random patient-level split is not metric-ready for all labels — see split feasibility report.

## Dataset Confirmed

| Property | Value |
|----------|-------|
| Dataset root | `D:\Dataset_Chexpert` |
| Train CSV rows | 223,414 |
| Valid CSV rows | 234 |
| Train images resolved | 223,414 |
| Missing image paths (train) | 0 |
| Unique train patients | 64,540 |
| Unique valid patients | 200 |
| Patient overlap train/valid | 0 |
| Label columns | 11 CheXpert labels confirmed |
| Patient ID source | Directory name in Path column |

## Recommended Sample Size for EXP-0017

**1,000 images** is the recommended starting size for the first true linear-probe training run. The 1,000-image candidate manifest has been created deterministically (seed 42) with preference for frontal chest X-rays.

A 5,000-image manifest can be created quickly if the 1k run succeeds.

## Recommended Labels for First Linear-Probe Training

All 11 CheXpert labels have usable samples in the 1k manifest, but patient-level splitting requires correction before true training:

**Labels requiring stratified or targeted split handling:** Atelectasis, Pneumonia, Lung Lesion (zero negatives in validation/test), plus Fracture and Lung Opacity (low negatives in validation/test).

All other labels (Consolidation, Pneumothorax, Edema, Pleural Effusion, Cardiomegaly, Enlarged Cardiomediastinum) have sufficient class representation for metric evaluation under the current random split.



## Labels Requiring Split Correction

The following labels lack both positive and negative samples in one or more splits under the current random patient-level 70/15/15 split:

- **Atelectasis**: test_negative=0, validation_negative=1 (below threshold 3)
- **Pneumonia**: validation_negative=0, test_negative=1 (below threshold 3)
- **Lung Lesion**: validation_negative=0, test_negative=0
- **Fracture**: validation_negative=1, test_negative=2 (both below threshold 3)
- **Lung Opacity**: validation_negative=2 (below threshold 3)

EXP-0017 is approved only after split correction (stratified patient-level split) or with per-label metric masking for these labels.

## Recommended Split Policy

- **Patient-level split** with seed 42
- Train/Validation/Test: 70/15/15
- No patient appears in more than one split
- Patient-level split is feasible, but the current random 70/15/15 split is not metric-ready for all labels. EXP-0017 should use stratified or targeted patient-level splitting, especially for labels with missing or low negative/positive representation in validation/test.

## Whether New RAD-DINO Embeddings Should Be Generated

**Yes.** New RAD-DINO embeddings should be generated for the selected manifest images. The EXP-0013 smoke test confirmed the embedding pipeline works on this hardware (i7-12700H CPU). For 1,000 images, estimated CPU runtime is approximately 15.06 minutes.

## GPU Recommendation

**GPU is optional for 1,000 images** (~15.06 min on CPU), but recommended for production throughput if moving to 5,000+ images.

## Remaining Blockers

- Split feasibility issue: 5 labels lack both positive and negative samples in all splits (see patient_split_feasibility_report.json). EXP-0017 requires stratified patient-level split or per-label metric masking.

## Uncertain Label Policy (Requires Codex/Human Decision)

The CheXpert dataset uses -1.0 for uncertain labels. Before EXP-0017 training, a policy decision is needed:

- **U-zeros**: Treat -1.0 as negative (0.0). Standard CheXpert approach.
- **U-ignore**: Exclude uncertain labels from loss computation.
- **U-ones**: Treat -1.0 as positive. Conservative but may increase false positives.

This decision affects the label distribution and should be documented in EXP-0017.

## Next Steps

1. Human/Codex approval of this readiness assessment.
2. Human/Codex decision on uncertain label policy (U-zeros recommended).
3. Proceed to EXP-0017: first true linear-probe training on the 1k manifest.
4. After EXP-0017, scale to 5k and full dataset as resources allow.

## Limitations

- This is a dataset readiness check only, not clinical evaluation.
- No RAD-DINO inference or model training was performed.
- Label distributions are based on the deterministic 1k sample; full-dataset distributions may differ.
- Runtime estimates extrapolate linearly from EXP-0013; actual performance may vary.
