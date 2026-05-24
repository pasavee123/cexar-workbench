# REVIEW.md

## Experiment: EXP-0016

**Date:** 2026-05-24
**Reviewer:** Pending Codex/human review

## Review Status: PENDING

## Automated Checks

| Check | Status |
|-------|--------|
| Dataset root readable | PASS |
| CSV files identified | PASS (train: 223,414 rows; valid: 234 rows) |
| Image paths resolve | PASS (100% resolution, 0 missing) |
| Candidate manifest created | PASS (1,000 images, seed 42) |
| Label distribution reported | PASS (all 11 labels) |
| Patient split feasible | PASS (982 patients, 70/15/15) |
| Runtime estimate written | PASS |
| EXP-0017 recommendation written | PASS |
| Command ledger complete | PASS (8 commands) |
| No production/dataset/historical modification | PASS |

## Items Requiring Review

1. **Uncertain label policy decision** for EXP-0017 (U-zeros recommended)
2. **Sample size confirmation** (1,000 recommended)
3. **Label selection for first training run** (all 11 or subset)
4. **Stratified sampling needs** for low-prevalence labels (Lung Lesion, Fracture, Pneumonia)

## Review Outcome

[To be completed by Codex or human reviewer]

- [ ] Approve - Proceed to EXP-0017
- [ ] Approve with changes
- [ ] Reject - Return to experiment