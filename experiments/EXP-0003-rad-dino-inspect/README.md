# EXP-0003: RAD-DINO Inspect

## Hypothesis
RAD-DINO should be tested as a frozen foundation backbone for CeXaR due to its chest-X-ray-specific pretraining, HF Transformers compatibility, and strong reproducibility documentation.

## Scope
- Inspect model card, license/terms, preprocessing, expected image size, embedding shape, and model loading API
- Identify whether a synthetic tensor or tiny local image smoke test is possible
- Compare assumptions against `manifests/03_transformer_baselines.md`
- Record what is public, gated, private, or not reproducible

## Dependencies
- Python 3.10+
- transformers
- huggingface_hub
- torch
- PIL

## References
- Manifest: `manifests/03_transformer_baselines.md`
- HF Model: https://huggingface.co/microsoft/rad-dino
- Paper: https://www.nature.com/articles/s42256-024-00965-w