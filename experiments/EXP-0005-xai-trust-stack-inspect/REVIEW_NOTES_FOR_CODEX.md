# REVIEW_NOTES_FOR_CODEX.md

## Priority Items for Codex Review
1. **XAI stack confirmed**: grad-cam, Captum, Quantus, CheXlocalize all available and MIT/BSD licensed.
2. **grad-cam + Captum**: Both passed synthetic smoke tests. Integration into CeXaR is low-risk.
3. **Quantus**: Installed but needs full dependency install for runtime metric computation.
4. **CheXlocalize**: Best for localization evaluation but requires dataset.

## Recommended Actions
1. Accept all four tools as `integration-candidate` for CeXaR's trust stack
2. Next step: Wire grad-cam + Captum into CeXaR's evaluation pipeline
3. Add Quantus for standardized fidelity metrics
4. Add CheXlocalize for localization validation when dataset is available