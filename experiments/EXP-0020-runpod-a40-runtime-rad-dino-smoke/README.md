# EXP-0020 RunPod RTX 6000 Ada Runtime RAD-DINO Smoke

## Purpose

Validate the EXP-0019 CeXaR image on a real RunPod NVIDIA RTX 6000 Ada Generation pod, then run a limited RAD-DINO 100-image embedding smoke test.

This experiment verifies runtime compatibility only. It must not perform model training, classification, AUROC/AUPRC evaluation, clinical validation, or production integration.

## Required Image

Use the full SHA tag from EXP-0019:

```text
ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858
```

The image name contains `a40` for historical continuity with EXP-0019. The hardware contract for EXP-0020 and later cloud experiments is NVIDIA RTX 6000 Ada Generation.

## Required RunPod Settings

- GPU: NVIDIA RTX 6000 Ada Generation
- Container image: full SHA tag above
- Volume mount path: `/workspace`
- Repository checkout path: `/root/cexar-workbench`
- Dataset path: `/workspace/chexpert_dataset_raw`
- Optional compatibility symlink: `/mnt/chexpert -> /workspace/chexpert_dataset_raw`
- SSH over exposed TCP enabled
- No credentials committed to the repository

## Success Definition

EXP-0020 passes only if:
- The container boots on RunPod RTX 6000 Ada.
- Runtime verification passes.
- PyTorch sees NVIDIA RTX 6000 Ada through CUDA.
- `/workspace` and `/workspace/chexpert_dataset_raw` are available.
- RAD-DINO embeddings are generated for exactly 100 images.
- Output embedding shape is `[100, 768]`.
