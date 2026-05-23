# EXP-0004: BiomedCLIP and CheXzero Inspect

## Hypothesis
BiomedCLIP and CheXzero should serve as zero-shot or representation baselines for CeXaR. BiomedCLIP offers strong open-ecosystem quality via HF/open_clip; CheXzero is a key zero-shot CXR benchmark.

## Scope
- Inspect model/repo availability
- Compare prompt format, preprocessing, checkpoint availability, license, and expected output
- Identify whether either candidate can run a smoke test without datasets
- Record which one is better suited as a benchmark, not as production infra

## Dependencies
- Python 3.10+
- open_clip (for BiomedCLIP)
- torch
- PIL

## References
- Manifest: `manifests/03_transformer_baselines.md`
- BiomedCLIP: https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224
- CheXzero: https://github.com/stanfordmlgroup/CheXzero