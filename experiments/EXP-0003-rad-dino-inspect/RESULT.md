# RESULT.md

## Verdict:
- [x] **benchmark-candidate** (for frozen backbone representation evaluation)

## Summary
RAD-DINO is a strong benchmark candidate. The model card, config, preprocessing, and embedding specs are fully documented on HuggingFace. We confirmed: ViT-B/14 architecture, 768-dim embeddings, 518x518 input, MIT license. Full weight download (~1GB) timed out in this session but is publicly accessible without gating.

## Findings
- **License**: MIT (open for research and commercial use)
- **Architecture**: Dinov2Model (ViT-B/14), 12 layers, 12 attention heads
- **Embedding dim**: 768
- **Image size**: 518x518, 3 channels
- **Patch size**: 14 (37x37 patches)
- **Preprocessing**: Resize → CenterCrop(518x518) → Rescale(1/255) → Normalize(mean=[0.5307,0.5307,0.5307], std=[0.2583,0.2583,0.2583]) → ConvertRGB
- **Weights**: Public on HF, ~1GB safetensors (model.safetensors + backbone_compatible.safetensors + dino_head.safetensors)
- **Pipeline**: image-feature-extraction (no classification head — requires linear probe or custom head)
- **Requirements**: transformers >= 4.41.0, PyTorch >= 2.4 (note: transformers 4.40.2 with PyTorch 2.0.1 failed)
- **Maintenance**: Active — HF downloads ~400K, last updates visible

## Risks
- Full weight download is ~1GB, requires approval for this session
- Requires PyTorch >= 2.4 (current env has 2.0.1)
- ViT-B/14 patch size (14px) may be coarse for small pathology detection at 518px
- No built-in classifier — needs a custom linear probe/MLP head
- Public checkpoint does NOT exactly match the paper (paper used private data mix)

## Next Steps
- Recommend as `benchmark-candidate` for frozen backbone experiments
- Full forward-pass smoke test requires PyTorch upgrade and ~1GB weight download
- Compare with BiomedCLIP (EXP-0004) for backbone selection