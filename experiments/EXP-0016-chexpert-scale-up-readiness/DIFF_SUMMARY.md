# DIFF_SUMMARY.md

## Experiment: EXP-0016

**Date:** 2026-05-24
**Correction pass:** 2026-05-24 (Codex review)

## Files Created (Initial Run)

| File | Purpose |
|------|---------|
| `artifacts/run_chexpert_scale_up_readiness.py` | Main analysis script (all 6 phases) |
| `artifacts/dataset_inventory_report.json` | Phase 1: Dataset structure and counts |
| `artifacts/candidate_manifest_1k.csv` | Phase 2: 1,000-image deterministic manifest |
| `artifacts/label_distribution_report.json` | Phase 3: Per-label positive/negative/uncertain/missing counts |
| `artifacts/patient_split_feasibility_report.json` | Phase 4: Split feasibility with per-label checks |
| `artifacts/candidate_split_manifest_1k.csv` | Phase 4: Manifest with train/val/test split assignments |
| `artifacts/scale_up_runtime_estimate.md` | Phase 5: Runtime/storage estimates for 1k/5k/10k |
| `artifacts/EXP0017_READINESS.md` | Phase 6: EXP-0017 readiness recommendation |

## Files Modified (Initial Run)

| File | Change |
|------|--------|
| `commands.ps1` | Appended 8 commands (CMD-001 through CMD-008) with purpose, directory, destructive status, and results |
| `EXPERIMENT_LOG.md` | Replaced empty template with full chronological log |
| `RESULT.md` | Replaced template with PASS result |
| `FAILURE_REPORT.md` | Replaced template with no-failure confirmation |

## Correction Pass (Codex Review)

### Files Modified

| File | Change |
|------|--------|
| `artifacts/run_chexpert_scale_up_readiness.py` | Fixed `needs_stratified_sampling` logic in phase4 to check both positive AND negative counts with zero detection; updated phase6 result to PARTIAL PASS; added blocker text for split issues |
| `artifacts/patient_split_feasibility_report.json` | Regenerated with corrected logic: 5 labels now flagged (Atelectasis, Pneumonia, Lung Lesion, Fracture, Lung Opacity) with per-label reason fields |
| `artifacts/EXP0017_READINESS.md` | Result changed to PARTIAL PASS; split correction requirements added; label detail table included |
| `RESULT.md` | Result changed to PARTIAL PASS; split table updated with partial status; recommendations updated |
| `FAILURE_REPORT.md` | Added Codex Review Correction section with full correction details |
| `REVIEW_NOTES_FOR_CODEX.md` | Added correction pass status, split feasibility detail table |
| `EXPERIMENT_LOG.md` | Appended Correction Pass section |
| `DIFF_SUMMARY.md` | This file - added correction pass section |
| `commands.ps1` | Added CMD-009 (correction re-run) and AUDIT-BACKFILL-001 for unrecoverable CMD-007 text |
| `REVIEW.md` | Existed from initial run (unchanged in correction) |

## Files NOT Modified

All prior experiment directories (EXP-0012B, EXP-0013, EXP-0014, EXP-0015) were not touched.
Production code was not touched.
`D:\Dataset_Chexpert` was not modified (read-only access).
`.venvs/cexar-foundation` had only pandas==2.2.2 added during initial run (human-approved).

## Dependencies Changed

- Added `pandas==2.2.2` to `.venvs/cexar-foundation` (initial run only, with transitive deps: python-dateutil, pytz, tzdata, six)
- No additional packages installed during correction pass