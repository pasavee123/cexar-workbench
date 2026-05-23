# RESULT.md

## Verdict:
- **BiomedCLIP**: `integration-candidate` (for representation/zero-shot benchmark)
- **CheXzero**: `benchmark-candidate` (for zero-shot comparator, NOT for infra)

## Summary
BiomedCLIP loaded successfully via open_clip (MIT license, ~196M params, 512-dim embeddings, 224x224 input). Forward pass on synthetic tensor succeeded. CheXzero repo inspected — requires older stack (torch 1.10.2), HDF5 data format, and separate checkpoint download. Both are viable for benchmarking but NOT as production infrastructure.

## BiomedCLIP Findings
- **License**: MIT (open research + commercial)
- **Architecture**: ViT-B/16 vision encoder + PubMedBERT text encoder
- **Embedding dim**: 512
- **Image size**: 224x224
- **Input channels**: RGB (3)
- **Preprocessing**: CLIP standard (mean=[0.481, 0.458, 0.408], std=[0.269, 0.261, 0.276])
- **Total params**: ~196M
- **Loading**: via `open_clip.create_model_and_transforms('hf-hub:microsoft/BiomedCLIP-...')`
- **HF downloads**: ~954K (very popular, well-maintained)
- **Synthetic test**: Forward pass produces [1, 512] features successfully
- **Data pipeline**: Has separate official data pipeline repo

## CheXzero Findings
- **License**: MIT
- **Architecture**: CLIP ViT-B/32 (from OpenAI's clip package)
- **Image resolution**: 320x320
- **Embedding dim**: 768
- **Preprocessing**: Resize 320 → CenterCrop → Normalize (CLIP defaults)
- **Stack**: torch 1.10.2, torchvision 0.11.3 — very old, would conflict with CeXaR's current PyTorch 2.0.1
- **Data format**: HDF5 (`test_cxr.h5`) with shape (N, 320, 320) grayscale
- **Checkpoints**: Need to download from Google Drive (per manifest)
- **Maintenance**: Last updated May 2026, but pinned to old deps
- **Stars**: 225

## Risks
- **CheXzero**: PyTorch 1.10.2 vs current 2.0.1 creates dependency conflict. Cannot run in-session without env isolation.
- **CheXzero**: Requires MIMIC-CXR HDF5 data (~100GB+) for full eval — blocked without approval.
- **BiomedCLIP**: Uses CLIP normalization (ImageNet), not CXR HU normalization. Must not be mixed with XRV-style preprocessing.
- **BiomedCLIP**: ~196M params — moderate GPU memory needed.

## Next Steps
- Use BiomedCLIP (via open_clip) for zero-shot baselines in CeXaR
- Use CheXzero only as paper reference comparator, not for infra reuse
- Both should be `benchmark-candidate` but BiomedCLIP is notably easier to integrate