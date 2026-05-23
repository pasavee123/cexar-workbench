# Environment Side Effects

## Python Availability

Python is NOT available in the current Pro review shell. The following is compiled from Flash's EXPERIMENT_LOG.md and DIFF_SUMMARY.md files across all experiments.

## Packages Installed by Flash

| Package | Version | Experiment | Method | Note |
|---|---|---|---|---|
| torchxrayvision | 1.4.0 | EXP-0002 | `pip install` | Normal install |
| transformers | 5.9.0 → downgraded to 4.40.2 | EXP-0003 | `pip install` then downgrade | 4.40.2 is PyTorch 2.0.1 compatible |
| huggingface_hub | (latest) | EXP-0003 | `pip install transformers huggingface_hub` | Required for HF model card inspection |
| open_clip_torch | 3.3.0 | EXP-0004 | `pip install open_clip_torch` | Used to load BiomedCLIP |
| grad-cam | 1.5.5 | EXP-0005 | `pip install --no-deps` | CNN/ViT CAM generation |
| captum | 0.9.0 | EXP-0005 | `pip install --no-deps` | IntegratedGradients attributions |
| quantus | 0.6.0 | EXP-0005 | `pip install --no-deps` | XAI evaluation metrics (no smoke test run) |
| ttach | 0.0.3 | EXP-0005 | `pip install --no-deps` | Dependency for grad-cam |
| MONAI | 1.5.2 | EXP-0006 | `pip install monai` | Medical imaging transforms + determinism |
| hydra-core | 1.3.2 | EXP-0006 | `pip install hydra-core` | Config composition |
| antlr4-python3-runtime | (auto) | EXP-0006 | Auto-dep of hydra-core | Hydra config parser dependency |
| omegaconf | (auto) | EXP-0006 | Auto-dep of hydra-core | YAML config parsing |

## Packages Upgraded by Flash (CRITICAL)

| Package | From | To | Experiment | Risk |
|---|---|---|---|---|
| **PyTorch** | **2.0.1+cpu** | **2.12.0+cpu** | EXP-0006 | **HIGH** — Global upgrade. MONAI >=1.5.x requires PyTorch >=2.4.1, so pip auto-upgraded. This affects every other experiment and any pre-existing code expecting 2.0.1. torchvision extension rebuild warning was observed. |
| **timm** | **0.4.12** | **1.0.27** | EXP-0004 | **MEDIUM** — open_clip_torch 3.3.0 pulled timm >=1.x. Flash's own EXP-0004 DIFF_SUMMARY notes `segmentation-models-pytorch 0.2.1 expects timm==0.4.12` may be incompatible. |
| torchvision | (unknown) | (unknown) | EXP-0006 | **MEDIUM** — Likely upgraded alongside PyTorch. Extension rebuild warning noted in EXP-0006 log. |

## Model Weights / Cache Created

| Path | Size | Experiment | Content |
|---|---|---|---|
| `~/.torchxrayvision/models_data/` | ~447 MB | EXP-0002 | DenseNet121 weights from GitHub releases |
| `~/.cache/huggingface/hub/models--microsoft--rad-dino/` | config only (~KB) | EXP-0003 | config.json, preprocessor_config.json (weights NOT downloaded — timed out) |
| `~/.cache/huggingface/hub/models--microsoft--BiomedCLIP-.../` | config + partial | EXP-0004 | open_clip_config.json and example data. Model weights may be cached if full forward pass triggered download via open_clip. |
| `~/.cache/torch/hub/` | (unknown) | EXP-0005 | Possible grad-cam/captum caching |

## Changes Outside `experiments/`

| Path | Type | Risk |
|---|---|---|
| Global Python site-packages | Package installs/upgrades | **HIGH** — PyTorch, timm, torchvision upgraded globally. All 12+ new packages installed globally. No virtual environment was used. |
| `~/.torchxrayvision/` | Model weight cache | **LOW** — Expected side effect of XRV smoke test |
| `~/.cache/huggingface/` | HF cache | **LOW** — Expected side effect of HF API inspection |
| `~/.cache/torch/` | PyTorch hub cache | **LOW** — Expected side effect |
| `PYTHONIOENCODING` | Environment variable | **NONE** — Set per-command only, not persisted |

## Environment Risks Summary

1. **CRITICAL — PyTorch Major Version Jump**: 2.0.1 → 2.12.0 is an 11-minor-version leap. This breaks API compatibility with any code pinned to 2.0.x (e.g., `torch.compile` changes, `torch.set_default_device` behavior, quantization API changes). Any pre-existing CeXaR code, scripts, or dependencies that were tested on 2.0.1 are now running on an untested runtime.

2. **HIGH — timm Breakage Risk**: `segmentation-models-pytorch 0.2.1` (pre-installed) explicitly requires `timm==0.4.12`. The upgrade to `timm 1.0.27` may cause import errors or silent behavior changes. This is not tested and was flagged by Flash but not resolved.

3. **MEDIUM — No Environment Isolation**: All experiments ran in the same global Python environment. EXP-0006's PyTorch upgrade retroactively invalidates any assumptions made by EXP-0002 through EXP-0005 about their runtime environment. Experiments are not independently reproducible.

4. **MEDIUM — OpenCLIP Version Unknown**: Flash's logs mention `open_clip.create_model_and_transforms` working but do not record the open_clip_torch version. The DIFF_SUMMARY of EXP-0004 only says "timm 1.0.27 installed" without noting the open_clip version. Version 3.3.0 is assumed from pip install defaults.

5. **LOW — Quantus Runtime Dependencies**: Quantus was installed `--no-deps`. Its actual dependencies (numpy, scipy, scikit-image, opencv-python, etc.) may or may not be present. A full install test has not been performed. Flash acknowledges this risk.

## Recommended Cleanup / Isolation Plan

1. **Immediate**: Roll back PyTorch to 2.0.1 (or whatever version CeXaR production is pinned to). `pip install torch==2.0.1 torchvision==0.15.2 --force-reinstall`
2. **Immediate**: Roll back timm to 0.4.12. `pip install timm==0.4.12 --force-reinstall`
3. **Before any next experiment**: Create a project-level `requirements.txt` or `pyproject.toml` with pinned versions.
4. **Before any next install-heavy experiment**: Use a virtual environment or conda environment. Document the env creation command in EXPERIMENT_LOG.md.
5. **After rollback**: Rerun the EXP-0002 TorchXRayVision smoke test to confirm XRV still works on PyTorch 2.0.1 (it was confirmed on 2.0.1 originally).
6. **For EXP-0006 rerun**: Isolate in a venv with PyTorch 2.12.0 specifically — do not upgrade the global environment.