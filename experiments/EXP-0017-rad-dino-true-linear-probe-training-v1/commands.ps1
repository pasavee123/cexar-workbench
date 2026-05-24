# EXP-0017 command ledger
# Runner must append every exact terminal command before execution.
# Do not summarize multiple commands.

# --- CMD-001: Check venv Python version ---
# Purpose: Verify .venvs/cexar-foundation exists and Python version
# Working directory: D:\cexar-workbench
# Destructive: No
# COMMAND: .venvs\cexar-foundation\Scripts\python.exe --version
# EXIT CODE: 0
# RESULT SUMMARY: Python 3.10.2

# --- CMD-002: List venv installed packages ---
# Purpose: Verify torch, transformers, Pillow, numpy, pandas, scikit-learn available
# Working directory: D:\cexar-workbench
# Destructive: No
# COMMAND: .venvs\cexar-foundation\Scripts\pip.exe list
# EXIT CODE: 0
# RESULT SUMMARY: All required packages confirmed: torch 2.5.1, transformers 4.45.2, Pillow 12.2.0, numpy 1.26.4, pandas 2.2.2, scikit-learn 1.4.2, psutil 7.2.2, huggingface_hub 0.36.2

# --- CMD-003: Check RAD-DINO local cache ---
# Purpose: Verify RAD-DINO weights are locally cached
# Working directory: D:\cexar-workbench
# Destructive: No
# COMMAND: .venvs\cexar-foundation\Scripts\python.exe -c "import os; cache=os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub'); print('Cache exists:', os.path.isdir(cache)); models_dirs=[d for d in os.listdir(cache) if 'rad-dino' in d.lower()] if os.path.isdir(cache) else []; print('RAD-DINO dirs:', models_dirs); print('Weight source: local_cache' if models_dirs else 'Weight source: NOT FOUND')"
# EXIT CODE: 0
# RESULT SUMMARY: RAD-DINO weights found in local cache: [models--microsoft--rad-dino]. No network download needed.

# --- CMD-004: Verify manifest row count ---
# Purpose: Confirm candidate_manifest_1k.csv has exactly 1000 rows
# Working directory: D:\cexar-workbench
# Destructive: No
# COMMAND: .venvs\cexar-foundation\Scripts\python.exe -c "import csv; f=open(r'experiments\EXP-0016-chexpert-scale-up-readiness\artifacts\candidate_manifest_1k.csv','r'); reader=csv.DictReader(f); rows=list(reader); print('Rows (excl header):', len(rows)); print('Columns:', list(rows[0].keys()) if rows else 'N/A')"
# EXIT CODE: 1 (SyntaxError: f-string backslash)
# RESULT SUMMARY: Syntax error due to backslash in f-string. Retrying with corrected command.

# --- CMD-004b: Verify manifest row count (corrected) ---
# Purpose: Confirm candidate_manifest_1k.csv has exactly 1000 rows
# Working directory: D:\cexar-workbench
# Destructive: No
# COMMAND: .venvs\cexar-foundation\Scripts\python.exe -c "import csv; f=open(r'experiments\EXP-0016-chexpert-scale-up-readiness\artifacts\candidate_manifest_1k.csv','r'); reader=csv.DictReader(f); rows=list(reader); print('Rows (excl header):', len(rows)); cols = list(rows[0].keys()); print('Columns:', cols); label_cols = ['Atelectasis','Consolidation','Pneumothorax','Edema','Pleural Effusion','Pneumonia','Cardiomegaly','Lung Lesion','Fracture','Lung Opacity','Enlarged Cardiomediastinum']; present = [c for c in label_cols if c in cols]; print('CheXpert label columns present:', len(present), '/ 11')"
# EXIT CODE: 0
# RESULT SUMMARY: 1000 rows, 21 columns including all 11 CheXpert labels

# --- CMD-005: Check PyTorch device ---
# Purpose: Record whether CPU or CUDA is available
# Working directory: D:\cexar-workbench
# Destructive: No
# COMMAND: .venvs\cexar-foundation\Scripts\python.exe -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Device:', 'cuda' if torch.cuda.is_available() else 'cpu')"
# EXIT CODE: 0
# RESULT SUMMARY: PyTorch 2.5.1+cpu, CUDA not available, device=cpu

# --- CMD-006: Run EXP-0017 experiment script (Phases 1-5) ---
# Purpose: Execute all experiment phases: validation, split, embeddings, probes, baseline
# Working directory: D:\cexar-workbench
# Destructive: No (writes artifacts only)
# COMMAND: .venvs\cexar-foundation\Scripts\python.exe experiments\EXP-0017-rad-dino-true-linear-probe-training-v1\artifacts\run_exp0017_true_linear_probe.py
# EXIT CODE: 0
# RESULT SUMMARY: All phases completed. 1000/1000 embeddings succeeded (100%, 1161.52s). 10/11 labels fully trainable, 1 masked (Fracture val_pos=1). Train AUROC=1.0 on all labels (overfitting expected). Best test AUROC: Pneumothorax 0.7887.
