# REVIEW.md

## Experiment: EXP-0015 — RAD-DINO Linear Probe Smoke Test

### Status: READY FOR CODEX REVIEW

### Review Checklist

- [x] All protocol documents read; one command-ledger compliance limitation is documented via audit backfill
- [x] All required artifact files present and validated
- [x] Command ledger (commands.ps1) contains 5 recorded commands plus documented audit backfill entries for 2 failed attempts whose exact terminal text was not recorded at execution time
- [x] EXPERIMENT_LOG.md updated with full chronological log
- [x] RESULT.md states result: PASS AS LINEAR PROBE SMOKE TEST
- [x] FAILURE_REPORT.md written (no blocking failures)
- [x] DIFF_SUMMARY.md written with all file changes
- [x] REVIEW_NOTES_FOR_CODEX.md written
- [x] No production code modified
- [x] No prior experiment artifacts modified
- [x] No unsupported clinical claims
- [x] pipeline_sanity_note present on all metrics
- [x] Wrong-path incident documented (no unauthorized cleanup)

### Key Results

8 of 11 CheXpert labels completed the linear probe smoke test on frozen RAD-DINO embeddings with a deterministic patient-level split (seed=42, 79 train / 21 eval).

AUROC values (PIPELINE SANITY ONLY — NOT CLINICAL PERFORMANCE):
- Atelectasis: 0.7206
- Consolidation: 0.8421
- Edema: 0.3519
- Pleural Effusion: 0.7000
- Pneumonia: 1.0000 (3 total positives — unreliable)
- Cardiomegaly: 0.5000
- Lung Opacity: 0.7019
- Enlarged Cardiomediastinum: 0.6818

### Decision Required

Approve/reject the smoke test result and decide on next steps (scale-up, GPU embeddings, stratified split).
