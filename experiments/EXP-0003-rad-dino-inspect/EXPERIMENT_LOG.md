# EXPERIMENT_LOG.md

## Session 1 — RAD-DINO Inspection

### [2026-05-22 20:34] Step 1: Install transformers & huggingface_hub
- **WD:** `D:\cexar-workbench`
- **Command:** `pip install transformers huggingface_hub`
- **Exit:** 0
- **Stdout:** transformers 5.9.0 installed
- **Interpretation:** Initial install succeeded but 5.9.0 requires PyTorch >= 2.4

### [2026-05-22 20:35] Step 1b: Downgrade transformers for PyTorch 2.0.1 compat
- **WD:** `D:\cexar-workbench`
- **Command:** `pip install "transformers>=4.30.0,<4.41.0"`
- **Exit:** 0
- **Stdout:** transformers 4.40.2 installed
- **Interpretation:** Compatible transformers version installed.

### [2026-05-22 20:36] Step 2: Try loading RAD-DINO model (timed out)
- **WD:** `D:\cexar-workbench`
- **Command:** `AutoModel.from_pretrained('microsoft/rad-dino')`
- **Exit:** TIMEOUT (300s)
- **Interpretation:** Model weights ~1GB, download exceeded session timeout. This is expected per experiment protocol (large weights need approval).

### [2026-05-22 20:39] Step 3: Inspect model card via HF API
- **WD:** `D:\cexar-workbench`
- **Command:** `model_info('microsoft/rad-dino')`
- **Exit:** 0
- **Stdout:** Model ID: microsoft/rad-dino, Author: microsoft, License: MIT, Pipeline: image-feature-extraction, Downloads: ~400K
- **Interpretation:** Model is public, MIT licensed, well-maintained.

### [2026-05-22 20:40] Step 4: List repo files & read config
- **WD:** `D:\cexar-workbench`
- **Command:** `list_repo_files`, `hf_hub_download` for config.json and preprocessor_config.json
- **Exit:** 0
- **Stdout:** 
  - config.json: Dinov2Model, hidden_size=768, num_layers=12, num_heads=12, image_size=518, patch_size=14
  - preprocessor_config.json: Resize→CenterCrop(518x518)→Rescale(1/255)→Normalize(mean=[0.5307], std=[0.2583])→ConvertRGB
  - Files: model.safetensors (~900MB), backbone_compatible.safetensors, dino_head.safetensors, augmentations.py, config.json, preprocessor_config.json, pyproject.toml, training_images.csv, vitb14_cxr.yaml
- **Interpretation:** All preprocessing and model config documented. Forward pass requires ~1GB download and PyTorch >= 2.4.