# REVIEW_NOTES_FOR_CODEX.md

## Experiment: EXP-0016

**Result:** PARTIAL PASS AS SCALE-UP READINESS CHECK
**Date:** 2026-05-24
**Correction pass completed:** 2026-05-24

## What This Experiment Confirmed

1. **Dataset integrity:** D:\Dataset_Chexpert\archive contains 223,414 train images and 234 valid images with complete CSV metadata. All image paths resolve (0 missing).

2. **Label coverage:** All 11 CheXpert labels have usable positive and negative samples in a 1,000-image deterministic sample.

3. **Patient-level splits are structurally feasible:** 982 unique patients in the 1k manifest. No cross-split patient overlap with 70/15/15 split.

4. **Current random patient split is not metric-ready for all labels.** Atelectasis, Pneumonia, and Lung Lesion have zero negatives in validation or test. Fracture and Lung Opacity have negatives below threshold in some splits. EXP-0017 should require stratified patient-level split or per-label metric masking.

5. **Scale estimates:** CPU-only embedding generation is practical for 1,000 images (~15 min). GPU recommended for 5,000+.

## Correction Pass Completed

After Codex review identified split feasibility interpretation errors:

- Corrected `needs_stratified_sampling` logic to check both positive AND negative counts with proper zero detection and threshold checks (train<5, val<3, test<3).
- Re-ran analysis script (CMD-009) to regenerate `patient_split_feasibility_report.json` and `EXP0017_READINESS.md`.
- Updated all documentation files: RESULT.md (PARTIAL PASS), FAILURE_REPORT.md (Codex section), EXPERIMENT_LOG.md, DIFF_SUMMARY.md, REVIEW_NOTES_FOR_CODEX.md.
- Added AUDIT-BACKFILL-001 to commands.ps1 for unrecoverable CMD-007 command text.
- No training, inference, embedding generation, or dataset modification was performed.

## Split Feasibility Detail (Post-Correction)

| Label | Issue | Split(s) Affected |
|-------|-------|-------------------|
| Atelectasis | test_negative=0, validation_negative=1 (<3) | test, validation |
| Pneumonia | validation_negative=0, test_negative=1 (<3) | validation, test |
| Lung Lesion | validation_negative=0, test_negative=0 | validation, test |
| Fracture | validation_negative=1 (<3), test_negative=2 (<3) | validation, test |
| Lung Opacity | validation_negative=2 (<3) | validation |

## Decisions Needed Before EXP-0017

1. **Uncertain label policy:** The CheXpert dataset uses -1.0 for uncertain labels. Three options:
   - **U-zeros** (recommended): Treat -1.0 as negative. Standard CheXpert approach.
   - **U-ignore**: Mask uncertain labels during loss computation.
   - **U-ones**: Treat -1.0 as positive (conservative).

2. **Sample size confirmation:** 1,000 images recommended for first linear-probe run. A 5,000-image manifest can be generated from the same pool if desired.

3. **Split strategy:** EXP-0017 must use stratified patient-level splitting or per-label metric masking for Atelectasis, Pneumonia, Lung Lesion, Fracture, and Lung Opacity.

4. **Label selection:** All 11 labels or a subset? Low-prevalence labels (Lung Lesion: 44 pos, Fracture: 37 pos, Pneumonia: 32 pos in 1k manifest) may benefit from oversampling or binarized training.

## Artifacts for Review

- `artifacts/candidate_manifest_1k.csv` - Ready-to-use manifest
- `artifacts/candidate_split_manifest_1k.csv` - Manifest with split assignments (random, not stratified)
- `artifacts/patient_split_feasibility_report.json` - Corrected split feasibility with per-label reasons
- `artifacts/EXP0017_READINESS.md` - Readiness recommendation with split correction requirements