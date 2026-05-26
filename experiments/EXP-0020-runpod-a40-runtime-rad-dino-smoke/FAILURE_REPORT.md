# FAILURE_REPORT.md

## Summary

No blocking failures occurred during EXP-0020. The experiment completed successfully.

## Non-Blocking Incidents

### INC-001: Path Mapping Correction (Phase 2)

- **Step:** CMD-015 — initial path verification with `--windows-prefix "D:\Dataset_Chexpert"`.
- **Issue:** 0/200 mapped images readable. The dataset on `/workspace/chexpert_dataset_raw` has `train/` and `valid/` at root, without an `archive/` directory. The manifest paths include `archive/` in the Windows prefix.
- **Resolution:** Corrected `--windows-prefix` to `D:\Dataset_Chexpert\archive` (CMD-016, CMD-017). All 100 images resolved and loaded successfully.
- **Impact on results:** None — this was a configuration adjustment, not a data or model issue.
- **Recommended follow-up:** Update `DATA_ASSET_MANIFEST.md` to document that the Windows → cloud mapping must include `archive/` in the prefix if the dataset lacks an `archive/` directory.

### INC-002: nvcc Not Available (Phase 1)

- **Step:** CMD-005 — `nvcc --version`.
- **Issue:** nvcc not found in PATH. CUDA compiler tools not installed in the container.
- **Resolution:** CUDA runtime verified through PyTorch (`torch.cuda.is_available()` returns True, device reports NVIDIA RTX 6000 Ada Generation).
- **Impact on results:** None — nvcc is a development tool, not required for PyTorch inference.
- **Recommended follow-up:** If CUDA compilation (e.g., custom CUDA kernels) is needed in future experiments, the image should include the CUDA toolkit or nvcc.

### INC-003: HF_HOME / TORCH_HOME Not Pre-Set (Phase 1)

- **Step:** CMD-006 — `verify_environment.py`.
- **Issue:** The environment variables HF_HOME and TORCH_HOME are not set to `/workspace/.cache/...` by default in the image.
- **Resolution:** Set manually via `export` before running the smoke script (CMD-017). Cache directories created under `/workspace/.cache/`.
- **Impact on results:** None — model weights downloaded successfully to `/workspace/.cache/huggingface` (339M).
- **Recommended follow-up:** Consider setting these variables in the Dockerfile or a startup script for future experiments.

### INC-004: du Timing Out on Network Volume (Phase 1)

- **Step:** CMD-008 — `du -sh`.
- **Issue:** `du` command timed out after 120s on the network volume.
- **Resolution:** Dataset existence verified via `ls` and image path resolution; sizes not measured.
- **Impact on results:** None — the 100-image test confirmed read access.
