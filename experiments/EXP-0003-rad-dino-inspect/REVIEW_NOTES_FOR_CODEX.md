# REVIEW_NOTES_FOR_CODEX.md

## Priority Items for Codex Review
1. **EXP-0003 complete**: RAD-DINO is a `benchmark-candidate` for frozen backbone.
2. **Weight download**: ~1GB from HuggingFace. Needs session approval or download outside session.
3. **PyTorch 2.4+ required**: Current environment has PyTorch 2.0.1. Upgrade needed for full smoke test.
4. **MIT license**: Safe for research and commercial use.

## Open Questions
- Should RAD-DINO be compared head-to-head with BiomedCLIP and TorchXRayVision in a unified benchmark?
- Linear probe config: what CeXaR labels/datasets should anchor the evaluation?

## Recommended Actions
1. Accept as `benchmark-candidate`
2. Prioritize PyTorch upgrade to 2.4+ for full forward-pass test
3. Proceed to EXP-0004 (BiomedCLIP/CheXzero) for comparative assessment