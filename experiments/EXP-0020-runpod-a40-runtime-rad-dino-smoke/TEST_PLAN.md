# TEST_PLAN.md

## Scope

EXP-0020 validates the EXP-0019 custom image on RunPod A40 and runs a 100-image RAD-DINO embedding smoke test.

Allowed:
- SSH into the RunPod pod.
- Clone/pull this repository under `/workspace/cexar-workbench`.
- Verify runtime environment.
- Verify dataset mount and sample image paths.
- Download or use cached RAD-DINO weights.
- Generate 100 RAD-DINO embeddings.
- Record runtime, GPU, VRAM, memory, image success count, and embedding shape.

Forbidden:
- No model training.
- No classifier/probe fitting.
- No AUROC/AUPRC or clinical metric calculation.
- No clinical claims.
- No production code edits.
- No dataset upload unless the human explicitly approves outside this plan.
- No secrets, SSH keys, hostnames, PATs, or private IPs in repo files.

## Required Inputs

- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0019-custom-a40-environment-build/RESULT.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/runpod_runtime_contract.yaml`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/DATA_ASSET_MANIFEST.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/network_volume_layout.yaml`
- `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv`

## Phase 0: Safety and Ledger

1. Read all required files.
2. Register every terminal command in `commands.ps1` before execution.
3. Update `EXPERIMENT_LOG.md` after each meaningful sub-step.
4. Do not run any hidden cleanup, copy, move, delete, or registry command.

## Phase 1: RunPod Container Boot Verification

Verify:

```bash
pwd
hostname
nvidia-smi
python --version
nvcc --version
python /opt/cexar/verify_environment.py
df -h /workspace
du -sh /workspace/chexpert_dataset_raw
du -sh /workspace/nih_dataset_raw
```

The human reports combined dataset usage is approximately 66G. If `du -sh` reports substantially different sizes, record the exact values in `EXPERIMENT_LOG.md` and continue only if at least 100 required CheXpert images are readable.

Expected:
- GPU: NVIDIA A40
- Python: 3.10.x
- CUDA build: 12.1
- torch: 2.3.1+cu121
- torchvision: 0.18.1+cu121
- `/workspace` writable
- `/workspace/chexpert_dataset_raw` readable
- `/workspace/nih_dataset_raw` readable

## Phase 2: Repository and Manifest Verification

Verify the repository is available at:

```text
/workspace/cexar-workbench
```

Verify manifest exists:

```text
experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv
```

Verify at least 100 manifest rows map to readable image files under:

```text
/workspace/chexpert_dataset_raw/archive
```

Optional compatibility setup:

```bash
mkdir -p /mnt
ln -sfn /workspace/chexpert_dataset_raw /mnt/chexpert
```

Only create this symlink after registering the exact command in `commands.ps1`.

## Phase 3: RAD-DINO 100-Image Embedding Smoke

Run `artifacts/run_exp0020_rad_dino_gpu_smoke.py` with:

- sample size: 100
- device: CUDA only
- expected GPU: NVIDIA A40
- expected embedding dimension: 768
- no labels, classifiers, metrics, or clinical claims

Expected outputs:

```text
artifacts/rad_dino_cloud_smoke_summary.json
artifacts/rad_dino_cloud_smoke_embeddings.npz
```

## Phase 4: Result

Write:
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:
- GPU is not NVIDIA A40.
- CUDA is unavailable.
- `verify_environment.py` fails.
- `/workspace` is not writable.
- `/workspace/chexpert_dataset_raw` is missing or unreadable.
- fewer than 100 images are readable before inference.
- RAD-DINO embedding shape is not `[100, 768]`.
- any command was run without exact ledger recording.
