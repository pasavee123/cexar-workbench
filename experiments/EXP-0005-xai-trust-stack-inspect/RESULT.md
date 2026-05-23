# RESULT.md

## Verdict:
- **pytorch-grad-cam**: `integration-candidate`
- **Captum**: `integration-candidate`
- **Quantus**: `integration-candidate`
- **CheXlocalize**: `benchmark-candidate`

## Summary
All four tools are viable for CeXaR's explainability and fidelity validation stack. grad-cam and Captum passed synthetic tensor smoke tests. Quantus installs cleanly. CheXlocalize is MIT-licensed and recently updated.

## Findings

### pytorch-grad-cam v1.5.5
- **License**: MIT
- **API**: `GradCAM(model, target_layers)` — works with CNN and ViT
- **Smoke test**: Output shape (1, 64, 64) on synthetic CNN, values in [0, 1]
- **Risk**: Depends on `ttach` package; on Windows requires utf-8 encoding fix

### Captum v0.9.0
- **License**: BSD-3
- **API**: `IntegratedGradients(model)` — works with any PyTorch module
- **Smoke test**: IG attribution shape (1, 3, 64, 64), convergence delta ~1e-5
- **Risk**: None significant

### Quantus v0.6.0
- **License**: MIT
- **Available metrics**: Includes deletion/insertion AUC, pointing game, IoU, sanity checks, etc.
- **Risk**: May have troves of dependencies at runtime; verify with full install

### CheXlocalize
- **License**: MIT
- **Stars**: 40
- **Last updated**: 2026-05-22 (actively maintained)
- **Use**: Provides heatmap→segmentation conversion, mIoU, pointing game, bootstrap evaluation
- **Risk**: Requires dataset download (~668 test images) for full evaluation

## Next Steps
- All four tools should be integrated into CeXaR's trust evaluation pipeline
- Full integration requires mapping each tool's output format to CeXaR's heatmap/metadata schema