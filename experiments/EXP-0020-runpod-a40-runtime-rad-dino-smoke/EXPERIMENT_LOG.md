# EXPERIMENT_LOG.md

## 2026-05-26T17:10:16+00:00 — Run Start

Runner started. All required files read. Repository at /root/cexar-workbench, commit 518fe3e.

## 2026-05-26T17:11:17+00:00 — Phase 1: Environment Verification

**CMD-001 (pwd):** /root. Not using the repo directory as working directory for initial checks (shell defaults to /root).

**CMD-002 (hostname):** a8d97516fb6b

**CMD-003 (nvidia-smi):** GPU confirmed as NVIDIA RTX 6000 Ada Generation, 49140 MiB VRAM. Driver 550.127.05, CUDA 12.4.

**CMD-004 (python --version):** Python 3.10.12 from /opt/venv.

**CMD-005 (nvcc --version):** Not found. This is expected — CUDA runtime is available through PyTorch (12.1), driver supports 12.4.

**CMD-006 (verify_environment.py):**
- CUDA: available, device name NVIDIA RTX 6000 Ada Generation
- torch: 2.3.1+cu121, torchvision: 0.18.1+cu121
- python: 3.10.12
- All packages: numpy 1.26.4, pandas 2.2.2, pillow 10.4.0, psutil 6.0.0, scikit_learn 1.5.1, tqdm 4.66.4, transformers 4.41.2
- ENVIRONMENT_CONTRACT_FAILURES: HF_HOME not /workspace/.cache/huggingface, TORCH_HOME not /workspace/.cache/torch

**CMD-007 (df -h /workspace):** /workspace mounted from mfs#us-wa-1.runpod.net:9421, 479T total, 285T used, 194T available (60%).

**CMD-008 (du -sh):** Timed out after 120s on network volume. Dataset size cannot be measured via du.

**CMD-009 (ls):** CheXpert dataset has train/, train.csv, valid/, valid.csv. NIH14 has images_001 through images_012 plus metadata files.

**CMD-010 (find | wc -l):** Timed out after 120s on network volume.

**CMD-012 (mkdir cache dirs):** /workspace/.cache/huggingface and /workspace/.cache/torch created.

## 2026-05-26T17:12:00+00:00 — Phase 2: Manifest Verification

**CMD-013 (ls manifest):** /root/cexar-workbench/experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv exists, 143840 bytes.

**CMD-014 (inspect manifest):** 1000 rows. Columns: sample_index, resolved_path, patient_id, source_csv, csv_row_idx, Frontal/Lateral, Sex, Age, AP/PA, plus 14 CheXpert label columns, split_placeholder. Paths are Windows format (D:\Dataset_Chexpert\archive\train\...).

**CMD-015 (verify 100+ readable with original mapping):** 0/200 readable using D:\Dataset_Chexpert → /workspace/chexpert_dataset_raw mapping. Actual dataset structure lacks archive/ directory.

**CMD-016 (test corrected mapping):** Path mapping corrected: D:\Dataset_Chexpert\archive → /workspace/chexpert_dataset_raw. Test path resolves correctly and exists.

**Key finding:** The dataset on the network volume is laid out as `/workspace/chexpert_dataset_raw/train/patientXXXXX/...` without an intermediate `archive/` directory. The manifest paths include `archive/` in the Windows prefix. The windows-prefix argument to the smoke script must be `D:\Dataset_Chexpert\archive`, not `D:\Dataset_Chexpert`.

## 2026-05-26T17:13:00+00:00 — Phase 3: RAD-DINO Smoke Test

CMD-017 executed. Full 100-image embedding smoke test with corrected path mapping.

**Result:** PASS
- 100/100 images succeeded, 0 failed
- Embedding shape: [100, 768]
- Runtime: 13.44 seconds
- GPU: NVIDIA RTX 6000 Ada Generation (48,640.1 MiB VRAM)
- VRAM peak: 346.3 MB allocated, 750.0 MB reserved
- HF cache on /workspace: 339M
- Artifacts: rad_dino_cloud_smoke_summary.json (1,097 bytes), rad_dino_cloud_smoke_embeddings.npz (286,175 bytes)

## 2026-05-26T17:18:00+00:00 — Phase 4: Documentation Complete

All required documents written:
- RESULT.md: PASS AS RUNTIME AND RAD-DINO SMOKE
- FAILURE_REPORT.md: No blocking failures; 4 non-blocking incidents documented
- DIFF_SUMMARY.md: All file changes cataloged
- REVIEW_NOTES_FOR_CODEX.md: 5 review items listed
- commands.ps1: 17 commands registered with results

## 2026-05-26T17:18:00+00:00 — Phase 5: Branch Publishing

Preparing to commit and push to review branch exp/0020-runpod-smoke-result.
