# REVIEW_NOTES_FOR_CODEX.md

## Priority Items for Codex Review
1. **timm** and **open_clip** should be integrated as CeXaR's backbone registry / CLIP layer
2. **OpenCXR** and **EVA-X** are worth dedicated experiments
3. **MLflow vs W&B** decision should be made early for experiment tracking
4. Remaining candidates (BioViL-T, CXR-CLIP, MedCLIP) are safe to ignore as infra deps

## Recommended Actions
1. Accept timm and open_clip as integration candidates
2. Plan EXP-0008 (OpenCXR toolbox inspection) or EXP-0009 (EVA-X combined localization) for future
3. Decide MLflow vs W&B as team standard