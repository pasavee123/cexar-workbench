# EXPERIMENT_LOG.md

## Session 1 — BiomedCLIP & CheXzero Inspection

### [2026-05-22 20:53] Step 1: Inspect BiomedCLIP model card
- **WD:** `D:\cexar-workbench`
- **Command:** `model_info('microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')`
- **Exit:** 0
- **Stdout:** Model ID: microsoft/BiomedCLIP-PubMedBERT_256-..., Pipeline: zero-shot-image-classification, License: MIT, Downloads: ~954K
- **Interpretation:** Public, MIT-licensed, very popular model.

### [2026-05-22 20:53] Step 2: Read BiomedCLIP open_clip_config.json
- **WD:** `D:\cexar-workbench`
- **Command:** `hf_hub_download` for open_clip_config.json
- **Exit:** 0
- **Stdout:** embed_dim=512, vision=ViT-B/16@224, text=PubMedBERT context_length=256, preprocess=CLIP standard
- **Interpretation:** Config fully documented. 512-dim embeddings.

### [2026-05-22 20:54] Step 3: Load BiomedCLIP via open_clip
- **WD:** `D:\cexar-workbench`
- **Command:** `open_clip.create_model_and_transforms('hf-hub:microsoft/BiomedCLIP-...')`
- **Exit:** 0 (partial — model loaded but output_dim attr failed)
- **Interpretation:** Need to use model.encode_image() directly.

### [2026-05-22 20:55] Step 4: BiomedCLIP forward pass
- **WD:** `D:\cexar-workbench`
- **Command:** `model.encode_image(torch.randn(1,3,224,224))`
- **Exit:** 0
- **Stdout:** Image features shape [1, 512], feature norm ~82.85, total params ~196M
- **Interpretation:** Forward pass works on synthetic tensor.

### [2026-05-22 20:55] Step 5: CheXzero repo inspection
- **WD:** `D:\cexar-workbench`
- **Command:** GitHub API for rajpurkarlab/CheXzero
- **Exit:** 0
- **Stdout:** Stars=225, License=MIT, Updated=2026-05-18. Files: README, zero_shot.py, eval.py, model.py, requirements.txt, checkpoints/(empty). 
- **Interpretation:** Repo active but stack is old (torch 1.10.2, transformers 4.19.0).

### [2026-05-22 20:56] Step 6: CheXzero requirements.txt
- **WD:** `D:\cexar-workbench`
- **Command:** Raw GitHub content
- **Exit:** 0
- **Stdout:** Requires torch==1.10.2, torchvision==0.11.3, clip, h5py, albumentations
- **Interpretation:** Would conflict with current PyTorch 2.0.1 env. Needs separate venv.

### [2026-05-22 20:56] Step 7: CheXzero zero_shot.py analysis
- **WD:** `D:\cexar-workbench`
- **Command:** Raw GitHub content (first 100 lines)
- **Exit:** 0
- **Stdout:** Uses CLIP ViT-B/32, image_resolution 320, embed_dim 768, HDF5 data format
- **Interpretation:** Arch clear. Requires HDF5 dataset for full eval — blocked without data download.