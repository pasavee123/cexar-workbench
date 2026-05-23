# Global Environment Risk Report

## Current State (as of 2026-05-22, post-Flash EXP-0006)

| Metric | Value | Severity |
|---|---|---|
| Global PyTorch | **2.12.0+cpu** (upgraded from 2.0.1) | CRITICAL |
| Global timm | **1.0.27** (upgraded from 0.4.12) | HIGH |
| Global torchvision | Unknown — likely upgraded with PyTorch | MEDIUM |
| New packages in global site-packages | 12+ (transformers, open_clip, monai, hydra, grad-cam, captum, quantus, ttach, omegaconf, antlr4, huggingface_hub, tokenizers) | HIGH |
| Virtual environments | None created | CRITICAL |
| Environment isolation | None — all experiments shared global Python | CRITICAL |

## Immediate Risks

### Risk 1: PyTorch 2.12.0 API Breakage (CRITICAL)

PyTorch 2.0.1 → 2.12.0 spans 11 minor versions. Known breaking changes include:
- `torch.compile` API changes (default backends, options)
- `torch.set_default_device` behavior changes
- Quantization API deprecations and removals (torch.quantization → torch.ao.quantization)
- `torch.autograd.profiler` API changes
- ONNX export behavior differences

Any pre-existing CeXaR code or script that was tested on PyTorch 2.0.1 is now running on an untested PyTorch 2.12.0 runtime. Silent behavior changes (wrong outputs, no crash) are the most dangerous failure mode.

### Risk 2: timm 1.0.27 Breakage (HIGH)

`segmentation-models-pytorch 0.2.1` (pre-installed globally) explicitly pins `timm==0.4.12` in its setup.py. timm 1.x removed or renamed many internal APIs:
- `timm.models.layers.activations` → restructured
- `timm.models.resnet` → significant API changes
- Feature extraction interfaces changed

Import errors or silent weight loading failures are possible.

### Risk 3: No Reproducibility Audit Trail (HIGH)

No experiment can be reproduced from scratch because:
- The global environment state is not captured in any lockfile
- 12+ packages were installed without version pinning
- Package install order changed transitive dependency resolution
- No virtual environment provides a clean isolation boundary

### Risk 4: Quantus Runtime Failure (MEDIUM)

Quantus 0.6.0 was installed with `--no-deps`. Its runtime dependencies (scipy, scikit-image, opencv-python, etc.) may or may not be present. A `from quantus.metrics import FaithfulnessCorrelation` may fail with ImportError.

### Risk 5: Dormant Dependency Conflicts (LOW-MEDIUM)

The global environment now contains packages that are mutually incompatible:
- torch 2.12.0 + timm 1.0.27 + transformers 4.40.2 + open_clip 3.3.0 + monai 1.5.2 + torchxrayvision 1.4.0
- Some of these combinations were never tested together
- A seemingly unrelated `import` in a new experiment could trigger a latent conflict

## Required Mitigations

1. **Roll back global PyTorch to 2.0.1** before any experiment: `pip install torch==2.0.1 torchvision==0.15.2 --force-reinstall`
2. **Roll back global timm to 0.4.12**: `pip install timm==0.4.12 --force-reinstall`
3. **Set PIP_REQUIRE_VIRTUALENV=true** as a global environment variable to prevent accidental global installs
4. **Create all four venvs** as defined in ENV_PLAN.md before running any install-heavy experiment
5. **Add .venvs/ to .gitignore** to prevent venvs from being committed
6. **Verify global rollback** by running the EXP-0002 torchxrayvision smoke test after rollback