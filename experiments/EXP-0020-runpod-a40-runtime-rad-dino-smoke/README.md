# EXP-0020 RunPod A40 Runtime RAD-DINO Smoke

## Purpose

Validate the EXP-0019 CeXaR A40 image on a real RunPod NVIDIA A40 pod, then run a limited RAD-DINO 100-image embedding smoke test.

This experiment verifies runtime compatibility only. It must not perform model training, classification, AUROC/AUPRC evaluation, clinical validation, or production integration.

## Required Image

Use the full SHA tag from EXP-0019:

```text
ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858
```

## Required RunPod Settings

- GPU: NVIDIA A40
- Container image: full SHA tag above
- Volume mount path: `/workspace`
- Dataset mount path: `/mnt/chexpert`
- SSH over exposed TCP enabled
- No credentials committed to the repository

## Success Definition

EXP-0020 passes only if:
- The container boots on RunPod A40.
- Runtime verification passes.
- PyTorch sees NVIDIA A40 through CUDA.
- `/workspace` and `/mnt/chexpert` are available.
- RAD-DINO embeddings are generated for exactly 100 images.
- Output embedding shape is `[100, 768]`.

