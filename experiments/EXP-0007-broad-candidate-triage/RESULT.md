# EXP-0007 RESULT.md

## Candidate Triage Table

| Candidate | Purpose | License Risk | Maintenance | Dependency Risk | CeXaR Compatibility | Recommended Status |
|---|---|---|---|---|---|---|
| **OpenCXR** | Medical CXR toolbox (DICOM, preprocessing) | MIT (low) | Moderate (last commit Jan/Mar 2025) | Low (standalone toolbox) | Useful for DICOM/processing pipeline | `inspect-more` |
| **EVA-X** | CXR classification + segmentation + grad_cam | MIT (low) | Good (Dec 2025 commits) | Low (uses timm) | Strong for combined classification/localization experiments | `inspect-more` |
| **BioViL-T** | Multimodal CXR (image-text) | MIT (low) | Poor (hi-ml archived Nov 2025) | Low (HF transformers) | Weights useful; codebase archived | `reference-only` |
| **CheXFound** | Self-supervised CXR ViT | MIT (low) | Moderate (Sep 2025) | Medium (checkpoints on Google Drive) | Promising but artifacts not on HF yet | `inspect-more` |
| **CXR-CLIP** | CXR-specific CLIP | MIT (low) | Low (pinned to PyTorch 1.12) | High (old env) | Benchmark reference only | `reference-only` |
| **MedCLIP** | Medical CLIP (pip-installable) | MIT (low) | Low (code frozen Apr 2023) | Low (pip package) | Easy to try but stagnant | `reference-only` |
| **MS-CXR** | Phrase grounding benchmark | Dataset terms | N/A (dataset) | Low | Useful for multimodal evaluation | `reference-only` |
| **Transformer-Explainability** | ViT attention attribution | MIT (low) | Low (paper code) | Low | Research reference for ViT XAI | `reference-only` |
| **vit-explain** | ViT explanation methods | MIT (low) | Low (paper code) | Low | Research reference | `reference-only` |
| **saliency sanity-check repos** | Sanity check protocol | MIT (low) | Reference only | None | Protocol to adopt in CeXaR testing | `reference-only` |
| **MLflow** | Experiment tracking | Apache 2.0 (low) | Excellent (active 2026) | Medium (server setup) | Good for self-hosted lineage tracking | `inspect-more` |
| **W&B** | Experiment tracking + sweeps | Proprietary (medium) | Excellent | Low (SaaS) | Easier to start, but vendor lock-in risk | `inspect-more` |
| **Lightning** | Trainer orchestration | Apache 2.0 (low) | Excellent | Low | Optional; evaluator should not be locked to it | `inspect-more` |
| **timm** | Model registry/backbones | Apache 2.0 / MIT | Excellent (active 2026) | Low | HIGH value for backbone swapping | `integration-candidate` |
| **open_clip** | CLIP model loading/training | MIT (low) | Excellent (Feb 2026 release) | Low | HIGH value for CLIP-based experiments (confirmed in EXP-0004) | `integration-candidate` |

## Triage Summary

### Integration Candidates (ready for CeXaR)
- **timm**: Should be CeXaR's backbone registry for model swapping
- **open_clip**: Already confirmed in EXP-0004; use for CLIP-based benchmarks

### Inspect More (recommend dedicated experiments)
- **OpenCXR**: For DICOM/processing toolbox ideas
- **EVA-X**: Combined classification + localization experiments
- **CheXFound**: Next-generation CXR self-supervised model (when artifacts are on HF)
- **MLflow / W&B**: Experiment tracking — choose one as team standard
- **Lightning**: Optional trainer layer

### Reference Only
- **BioViL-T**: Archived codebase; weights usable
- **CXR-CLIP**: Old stack
- **MedCLIP**: Stagnant
- **MS-CXR**: Dataset for future multimodal eval
- **Transformer-Explainability, vit-explain**: Research references
- **saliency sanity-check repos**: Protocol to adopt

### No Rejects
- No candidate outright rejected — all have some reference value