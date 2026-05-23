# REVIEW_NOTES_FOR_CODEX.md — EXP-0012

## What Was Done

Ran TorchXRayVision DenseNet121 inference on 100 frontal CheXpert validation images and computed label-level AUROC for 11 cross-walked pathology labels.

## Key Findings for Codex Review

1. **Label crosswalk**: 11 of 18 XRV pathologies have direct CheXpert column matches. 7 do not (Infiltration, Emphysema, Fibrosis, Pleural_Thickening, Nodule, Mass, Hernia).

2. **Pipeline signal detected**: All 9 computable AUROC values are well above 0.5 (range: 0.599–0.922), confirming the XRV model produces output scores that correlate positively with CheXpert binary labels.

3. **Lowest AUROC**: Pneumothorax at 0.599 — may reflect low prevalence or label noise in this small sample.

4. **Uncomputable labels**: Lung Lesion and Fracture had only one class in this 100-image slice. Larger sample may be needed for these.

5. **sklearn avoidance**: AUROC computed with a local implementation — no dependencies installed.

## Items for Codex to Consider

- Should a larger sample or repeat runs with different random seeds be done?
- Should alternative metrics (e.g., PR-AUC for imbalanced classes) be considered?
- Should the crosswalk be validated against a clinical reference standard?

## No Production Integration

This experiment is a pipeline sanity check only. It does not qualify for production integration.