# EXP-0005: XAI Trust Stack Inspect

## Hypothesis
pytorch-grad-cam, Captum, Quantus, and CheXlocalize can form CeXaR's explainability and fidelity validation stack.

## Scope
- Inspect API compatibility with CNN and ViT models
- Identify minimal heatmap generation path
- Identify minimal heatmap evaluation path
- Map each tool to CeXaR outputs
- Check license and maintenance risk

## Dependencies
- Python 3.10+, torch, torchvision
- grad-cam, captum, quantus, chexlocalize

## References
- Manifest: `manifests/04_explainability_methods.md`, `05_fidelity_manifest.md`, `06_heatmap_validation.md`
- pytorch-grad-cam: https://github.com/jacobgil/pytorch-grad-cam
- Captum: https://github.com/pytorch/captum
- Quantus: https://github.com/understandable-machine-intelligence-lab/Quantus
- CheXlocalize: https://github.com/rajpurkarlab/cheXlocalize