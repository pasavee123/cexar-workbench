# commands.ps1

# Runner command ledger for EXP-0020.
# Every terminal command must be appended here before execution.
# Record exact command text, purpose, expected output, and result.

# --- Phase 1: RunPod Container Boot Verification ---

# CMD-001
# Purpose: Confirm current working directory
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# pwd

# CMD-002
# Purpose: Record hostname of the pod
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# hostname

# CMD-003
# Purpose: Verify GPU hardware via nvidia-smi
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# nvidia-smi

# CMD-004
# Purpose: Verify Python version from /opt/venv
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# source /opt/venv/bin/activate && python --version

# CMD-005
# Purpose: Verify CUDA compiler version
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# nvcc --version 2>&1 || echo "nvcc not found"
# Result: nvcc not found in PATH; CUDA 12.4 driver present via nvidia-smi.

# CMD-006
# Purpose: Run EXP-0019 environment verification script
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# source /opt/venv/bin/activate && python /opt/cexar/verify_environment.py

# CMD-007
# Purpose: Check /workspace mount and disk usage
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# df -h /workspace

# CMD-008
# Purpose: Measure dataset sizes
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# du -sh /workspace/chexpert_dataset_raw /workspace/nih_dataset_raw 2>&1
# Result: du timeout after 120s; need alternative measurement approach.

# CMD-009
# Purpose: Verify dataset directory structure exists
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# ls /workspace/chexpert_dataset_raw/ && ls /workspace/nih_dataset_raw/

# CMD-010
# Purpose: Count files in CheXpert dataset as alternative to du
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# find /workspace/chexpert_dataset_raw -type f | wc -l

# CMD-011
# Purpose: Set HF_HOME and TORCH_HOME for cache on network volume
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# export HF_HOME=/workspace/.cache/huggingface && export TORCH_HOME=/workspace/.cache/torch

# CMD-010
# Purpose: Count files in CheXpert dataset as alternative to du
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# find /workspace/chexpert_dataset_raw -type f | wc -l
# Result: Timeout after 120s on network volume; too many files to enumerate.

# CMD-012
# Purpose: Create cache directories on /workspace
# Working directory: /root/cexar-workbench
# Destructive: No (creates dirs, does not delete)
# Command:
# mkdir -p /workspace/.cache/huggingface /workspace/.cache/torch
# Result: Directories created successfully.

# --- Phase 2: Repository and Manifest Verification ---

# CMD-013
# Purpose: Check if manifest CSV exists
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# ls -la /root/cexar-workbench/experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv
# Result: Exists, 143840 bytes.

# CMD-014
# Purpose: Inspect manifest CSV columns and row count
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# source /opt/venv/bin/activate && python -c "import csv; ..."
# Result: 1000 rows, columns include sample_index, resolved_path, patient_id, 14 labels.

# CMD-015
# Purpose: Verify at least 100 mapped image paths are readable (with archive prefix)
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# source /opt/venv/bin/activate && python -c "..." 
# Result: 0 readable with windows_prefix=D:\\Dataset_Chexpert; dataset has no archive/ dir.

# CMD-016
# Purpose: Test corrected path mapping with archive in prefix
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# source /opt/venv/bin/activate && python -c "import os; ..."
# Result: Correct mapping is D:\\Dataset_Chexpert\\archive -> /workspace/chexpert_dataset_raw

# CMD-017
# Purpose: Run RAD-DINO 100-image embedding smoke test
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# source /opt/venv/bin/activate && export HF_HOME=/workspace/.cache/huggingface && export TORCH_HOME=/workspace/.cache/torch && python .../run_exp0020_rad_dino_gpu_smoke.py --manifest .../candidate_manifest_1k.csv --windows-prefix "D:\\Dataset_Chexpert\\archive" --cloud-prefix /workspace/chexpert_dataset_raw --model-id microsoft/rad-dino --limit 100 --output-summary .../rad_dino_cloud_smoke_summary.json --output-embeddings .../rad_dino_cloud_smoke_embeddings.npz
# Result: PASS. 100/100 images succeeded, embedding shape [100, 768], runtime 13.44s, GPU NVIDIA RTX 6000 Ada Generation, VRAM peak 750 MB reserved/346.3 MB allocated.

# --- Phase 5: Branch Publishing ---

# CMD-018
# Purpose: Check git status before committing
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# git status

# CMD-019
# Purpose: Check if target review branch already exists remotely
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# git ls-remote --heads origin exp/0020-runpod-smoke-result

# CMD-020
# Purpose: Create review branch and stage EXP-0020 changes
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# git checkout -b exp/0020-runpod-smoke-result && git add experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke

# CMD-021
# Purpose: Commit results to review branch
# Working directory: /root/cexar-workbench
# Destructive: No
# Command:
# git commit -m "record EXP-0020 RunPod RTX 6000 Ada smoke result"

# CMD-022
# Purpose: Push review branch to remote
# Working directory: /root/cexar-workbench
# Destructive: No (does not overwrite or delete)
# Command:
# git push origin exp/0020-runpod-smoke-result
