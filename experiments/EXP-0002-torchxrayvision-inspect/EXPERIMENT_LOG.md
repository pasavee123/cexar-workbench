# EXPERIMENT_LOG.md

## Session 1 — TorchXRayVision Inspection

### [2026-05-22 20:28] Step 1: Install torchxrayvision
- **WD:** `D:\cexar-workbench`
- **Command:** `python -m pip install torchxrayvision`
- **Exit:** 0
- **Stdout:** XRV v1.4.0 installed. Dependencies already satisfied: torch 2.0.1, torchvision 0.15.2, numpy, scikit-image, pandas, etc.
- **Stderr:** pip update notice only
- **Files:** None
- **Interpretation:** Clean install, no dependency conflicts.

### [2026-05-22 20:28] Step 2: Verify import
- **WD:** `D:\cexar-workbench`
- **Command:** `python -c "import torchxrayvision as xrv; print('XRV version:', xrv.__version__)"`
- **Exit:** 0
- **Stdout:** `XRV version: 1.4.0`
- **Stderr:** RequestsDependencyWarning (urllib3 version mismatch, non-critical)
- **Interpretation:** Import works.

### [2026-05-22 20:28] Step 3: Load DenseNet121 (first attempt — failed)
- **WD:** `D:\cexar-workbench`
- **Command:** `python -c "import torchxrayvision as xrv; model = xrv.models.get_model('densenet121-res224-all')"`
- **Exit:** 1
- **Error:** UnicodeEncodeError with progress bar character '\u2588' → partial download → corrupted weights (RuntimeError: unexpected EOF)
- **Interpretation:** First download failed due to Windows cp874 encoding. Corrupted file. Deleted and retried with PYTHONIOENCODING=utf-8.

### [2026-05-22 20:29] Step 3b: Load DenseNet121 (retry — succeeded)
- **WD:** `D:\cexar-workbench`
- **Command:** `PYTHONIOENCODING=utf-8 python -c "import torchxrayvision as xrv; model = xrv.models.get_model('densenet121-res224-all')"`
- **Exit:** 0
- **Stdout:** Model loaded as DenseNet. 18 pathologies listed.
- **Interpretation:** Model loads correctly with UTF-8 encoding.

### [2026-05-22 20:30] Step 4: Synthetic tensor forward pass
- **WD:** `D:\cexar-workbench`
- **Command:** Synthetic tensor [1,1,224,224] → model forward pass
- **Exit:** 0
- **Stdout:** Output shape [1, 18]. Sample logits: [0.605, 0.579, 0.530, ...]. Total params: 6,966,034.
- **Stderr:** Warning about input normalization range (expected for random tensor)
- **Interpretation:** Forward pass works. Output 18 logits matching 18 pathology classes.

### [2026-05-22 20:30] Step 5: Preprocessing and label audit
- **WD:** `D:\cexar-workbench`
- **Command:** Model config inspection
- **Exit:** 0
- **Interpretation:** Normalization confirmed [-1024, 1024] HU. Label order documented. Risk of mismatch with other repos confirmed.