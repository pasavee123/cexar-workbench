# RESULT.md

## Verdict:
- [x] **integration-candidate** (for baseline/data benchmark layer)

## Summary
TorchXRayVision v1.4.0 installs cleanly, loads pretrained DenseNet121 (6.97M params), and runs synthetic tensor forward passes with correct output shape [1, 18]. All 18 pathology labels are inspectable via `model.pathologies`. Preprocessing confirmed: [-1024, 1024] HU normalization, 224x224 input.

## Findings
- Package installed without dependency conflicts (torch 2.0.1, torchvision 0.15.2 already present)
- DenseNet121 weights downloaded and loaded successfully (447 MB)
- Forward pass on random tensor produces 18 logits
- Label order: 18 pathologies including Atelectasis, Consolidation, Infiltration, Pneumothorax, Edema, Emphysema, Fibrosis, Effusion, Pneumonia, Pleural_Thickening, Cardiomegaly, Nodule, Mass, Hernia, Lung Lesion, Fracture, Lung Opacity, Enlarged Cardiomediastinum
- Normalization must be [-1024, 1024] HU — NOT ImageNet normalization
- Warning when random tensor doesn't match expected HU range (expected behavior)

## Risks
- Normalization mismatch ([-1024, 1024] vs ImageNet) is the #1 risk when switching between XRV and other models
- Label order differs from CheXNet (arnoweng) and DacNet — label mapping must be explicit
- Weights downloaded from GitHub releases (~447 MB) — not from HuggingFace
- Unicode progress bar issue on Windows (workaround: PYTHONIOENCODING=utf-8)

## Next Steps
- Proceed to EXP-0003 (RAD-DINO) and EXP-0004 (BiomedCLIP/CheXzero) to complete baseline candidate assessment
- EXP-0002 recommends XRV as `integration-candidate` for CeXaR's baseline/data benchmark layer