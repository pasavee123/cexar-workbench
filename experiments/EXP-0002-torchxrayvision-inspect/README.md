# EXP-0002: TorchXRayVision Inspect

## Hypothesis
TorchXRayVision (XRV) should become CeXaR's baseline/data benchmark layer due to its unified API, common preprocessing chain, pretrained models, dataset wrappers, and distribution shift tools.

## Scope
- Inspect repository docs, license, installation path, model API, dataset wrappers, preprocessing assumptions, and label order
- Identify whether synthetic tensor smoke tests are possible without downloading datasets
- Try import/load-model smoke test if installation is lightweight
- Check whether output labels align with CeXaR manifest expectations
- Check risks around normalization mismatch and dataset harmonization

## Dependencies
- Python 3.10+
- torchxrayvision
- torch

## References
- Manifest: `manifests/01_baseline_manifest.md`
- Deep Research Report: `repo_hunt/candidates/deep-research-report.md`
- URL: https://github.com/mlmed/torchxrayvision