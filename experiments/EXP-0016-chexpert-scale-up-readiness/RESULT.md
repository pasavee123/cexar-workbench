# RESULT.md

## Experiment: EXP-0016

**Date:** 2026-05-24
**Runner:** Kilo (automated)

## Result: PARTIAL PASS AS SCALE-UP READINESS CHECK

This is a dataset scale-up readiness check only. No model training, RAD-DINO inference, embedding generation, or clinical evaluation was performed.

**Note:** This result was corrected from the initial "PASS" to "PARTIAL PASS" after Codex review identified that the split feasibility check did not properly flag labels lacking both positive and negative samples in all splits (see correction pass in EXPERIMENT_LOG.md).

## Evidence Summary

| Check | Status | Evidence |
|-------|--------|----------|
| Dataset root exists and readable | PASS | `D:\Dataset_Chexpert\archive\` with train.csv (223,414 rows) and valid.csv (234 rows) |
| Usable CSV identified | PASS | train.csv and valid.csv with Path column and 11 CheXpert label columns |
| Candidate manifest created deterministically | PASS | `candidate_manifest_1k.csv` with 1,000 images, seed 42, all frontal |
| Existing image-path rate measured | PASS | 223,414/223,414 train images resolve (100%); 0 missing |
| Label distribution reported | PASS | All 11 labels have positive and negative samples in the 1k manifest |
| Patient-level split feasibility reported | PASS (structural) | 982 unique patients, 70/15/15 split, no cross-split patient overlap |
| Metric readiness across all labels | PARTIAL | 5 labels (Atelectasis, Pneumonia, Lung Lesion, Fracture, Lung Opacity) lack both pos/neg samples in all splits; requires stratified split or per-label metric masking |
| Runtime/storage estimate written | PASS | ~15 min CPU for 1k embeddings, ~2.93 MB storage |
| EXP-0017 readiness recommendation written | PASS | Recommendation includes split correction requirements |
| All commands exact in commands.ps1 | PASS (with audit backfill) | 9 commands registered; 1 audit backfill for unrecoverable CMD-007 text |
| No dataset/production/prior-artifact modification | PASS | Read-only access only; all artifacts in experiment folder |

## Pass Criteria Evaluation

8 of 9 pass criteria fully met. Metric readiness across all labels is partial — see split feasibility report for details.

## Recommendations for EXP-0017

1. Start with 1,000-image manifest (already created deterministically)
2. Use patient-level split 70/15/15, seed 42, but with stratified or targeted splitting for affected labels
3. Labels requiring stratified split handling: Atelectasis, Pneumonia, Lung Lesion, Fracture, Lung Opacity
4. For single-label evaluation: all 11 labels are usable; for multi-label metrics, mask or correct splits for the 5 affected labels
5. Generate new RAD-DINO embeddings for the manifest images
6. Adopt U-zeros uncertain label policy (pending Codex/human decision)
7. GPU optional for 1k; recommended for >5k

## Limitations

- Label distribution reported for 1k sample only; full-dataset distribution may differ
- Runtime estimates extrapolate linearly from EXP-0013; actual performance may vary
- Uncertain label policy not yet decided (requires Codex/human input)
- This is a readiness check; no model training or clinical claims