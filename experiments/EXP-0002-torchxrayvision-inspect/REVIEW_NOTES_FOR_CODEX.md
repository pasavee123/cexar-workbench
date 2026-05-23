# REVIEW_NOTES_FOR_CODEX.md

## Priority Items for Codex Review
1. **XP-0002 complete**: TorchXRayVision is an `integration-candidate` for CeXaR's baseline/data benchmark layer.
2. **Normalization risk**: XRV uses [-1024, 1024] HU normalization. Any production code must NOT apply ImageNet normalization when using XRV.
3. **Label mapping**: The 18-label order differs from classic CheXNet/CheXpert repos. A label mapping table must be created in CeXaR before multi-repo integration.

## Open Questions
- Should CeXaR use XRV's model loading API directly, or wrap it in a CeXaR-native model registry?
- XRV weights come from GitHub releases (~447 MB). Should these be cached in a project-level model store?

## Recommended Actions
1. Accept XRV as `integration-candidate` for the baseline/data benchmark layer
2. Proceed with EXP-0003 (RAD-DINO) to compare another backbone candidate
3. Create label-harmonization config when integrating, using `model.pathologies` as the source of truth