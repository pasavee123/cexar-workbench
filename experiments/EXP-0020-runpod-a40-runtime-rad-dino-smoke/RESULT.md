# RESULT.md

## Final Status

**PASS AS RUNTIME AND RAD-DINO SMOKE**

EXP-0020 successfully validated the EXP-0019 CeXaR A40 image on an NVIDIA RTX 6000 Ada Generation pod and completed a 100-image RAD-DINO embedding smoke test. No training, classification, clinical metrics, or production integration occurred.

## Runtime Verification

| Check | Result |
|-------|--------|
| Image tag | `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858` |
| GPU model | NVIDIA RTX 6000 Ada Generation |
| VRAM total | 48,640.1 MiB |
| CUDA available | Yes (torch reports 12.1, driver 550.127.05 reports 12.4) |
| Python | 3.10.12 |
| torch | 2.3.1+cu121 |
| torchvision | 0.18.1+cu121 |
| transformers | 4.41.2 |
| /workspace mount | mfs#us-wa-1.runpod.net:9421, 479T total, 60% used |
| /workspace/chexpert_dataset_raw | Available, contains train/ and valid/ |
| /workspace/nih_dataset_raw | Available |
| /workspace/.cache/huggingface | Created, 339M after model download |
| nvcc | Not found in PATH (expected for runtime) |
| HF_HOME / TORCH_HOME | Not pre-set in image; set to /workspace/.cache/ during run |

## Path Mapping Correction

The CheXpert dataset on the network volume has train/ and valid/ at the dataset root (no intermediate archive/ directory). The EXP-0016 manifest uses Windows paths rooted at `D:\Dataset_Chexpert\archive\`. The smoke script was invoked with `--windows-prefix "D:\Dataset_Chexpert\archive" --cloud-prefix /workspace/chexpert_dataset_raw`.

## RAD-DINO Smoke Test

| Metric | Value |
|--------|-------|
| Model | microsoft/rad-dino |
| Model source | Downloaded to /workspace/.cache/huggingface |
| Images requested | 100 |
| Images attempted | 100 |
| Images succeeded | 100 |
| Images failed | 0 |
| Embedding shape | [100, 768] |
| Runtime | 13.44 seconds |
| GPU memory (after load) | 331.0 MB allocated, 382.0 MB reserved |
| GPU memory (after inference) | 346.3 MB allocated, 750.0 MB reserved |
| System RAM total | 1,511.56 GB |

## Pass/Fail Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Container boots on RTX 6000 Ada | PASS | CMD-003, CMD-006 |
| Runtime verification passes | PASS | CMD-004, CMD-006 |
| PyTorch sees CUDA with RTX 6000 Ada | PASS | CMD-006 (cuda_available: true, device_name_0: NVIDIA RTX 6000 Ada Generation) |
| /workspace available | PASS | CMD-007 |
| /workspace/chexpert_dataset_raw available | PASS | CMD-009 |
| 100+ CheXpert images readable | PASS | CMD-017 (100/100 succeeded) |
| Embedding shape is [100, 768] | PASS | CMD-017 output |
| No model training | PASS | training_performed: false |
| No clinical metrics | PASS | metrics_computed: false |
| No clinical claims | PASS | medical_claims: "none" |
| All commands logged in commands.ps1 | PASS | 17 commands registered |
| No secrets in repo files | PASS | Verified |

## Medical Claims Statement

In this experiment, RAD-DINO embeddings were extracted from 100 CheXpert images on a single GPU pod. No model training, classifier fitting, AUROC/AUPRC calculation, or clinical evaluation was performed. These results require clinical validation before any diagnostic interpretation. No clinical claims are made.

## Limitations

- Single pod, single run — not a reproducibility evaluation.
- 100-image sample does not cover dataset diversity, rare findings, or edge cases.
- No label-based evaluation or patient-level split validation.
- Path mapping required correction for dataset layout difference (archive/ mismatch).
- nvcc not available in the image; CUDA runtime verified through PyTorch.
- Environment variables HF_HOME and TORCH_HOME must be set manually to use /workspace cache.

## Artifacts

- `artifacts/rad_dino_cloud_smoke_summary.json` — Full run metadata (GPU, memory, timing, shape).
- `artifacts/rad_dino_cloud_smoke_embeddings.npz` — 100 × 768 float embeddings plus sample indices.
