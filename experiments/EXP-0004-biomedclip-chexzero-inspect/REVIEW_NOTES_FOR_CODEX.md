# REVIEW_NOTES_FOR_CODEX.md

## Priority Items for Codex Review
1. **BiomedCLIP**: Excellent `integration-candidate`. Easy to load via open_clip. MIT license. 512-dim embeddings. Use for zero-shot and representation benchmarks.
2. **CheXzero**: `benchmark-candidate` only. Too fragile for infra reuse — pinned to PyTorch 1.10.2.
3. **Label gap**: Neither model produces 18 CXR-specific labels like XRV. Requires prompt engineering (BiomedCLIP) or custom head.

## Open Questions
- Should CeXaR use BiomedCLIP's zero-shot prompts directly, or train a linear probe on top of its embeddings?
- CheXzero benchmarks are important for publications — should CeXaR maintain an isolated CheXzero env for this purpose?

## Recommended Actions
1. Accept BiomedCLIP as `integration-candidate` for representation/zero-shot benchmarking
2. Accept CheXzero as `benchmark-candidate` for paper comparison only
3. Proceed to EXP-0005 (XAI Trust Stack) for explainability assessment