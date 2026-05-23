# REVIEW_NOTES_FOR_CODEX.md

## Priority Items for Codex Review
1. **MONAI + Hydra**: Both confirmed working. Accept as `integration-candidate` for data/transform/cfg layer.
2. **PyTorch upgrade**: Now at 2.12.0. Verify torchvision extension compatibility.
3. **Seed policy**: Use `monai.set_determinism(seed)` as CeXaR's standard seed policy.

## Recommended Actions
1. Integrate MONAI transforms + Hydra config into CeXaR's experiment scaffold
2. Create standard CeXaR Hydra config template (dataset, model, eval, XAI blocks)
3. Proceed to EXP-0007 (Broad Candidate Triage)