# TEST_PLAN.md

## Scope

EXP-0019 validates the custom A40 environment build package only.

Allowed work:
- Review prior standards and EXP-0018 cloud readiness contract.
- Inspect and refine Dockerfile/startup scripts inside this experiment folder.
- Build the Docker image locally, in CI, or in an approved non-production builder.
- Verify package versions and runtime environment.
- Produce logs, result summaries, and failure reports.

Forbidden work:
- No RAD-DINO inference.
- No dataset upload.
- No model training.
- No AUROC/AUPRC evaluation.
- No clinical claims.
- No production code edits.
- No global Python modification.
- No unlogged cleanup, copy, move, delete, or registry operation.

## Required Inputs

- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0018-cloud-readiness-package/RESULT.md`
- `experiments/EXP-0018-cloud-readiness-package/cloud_provisioning_config.yaml`
- `experiments/EXP-0019-custom-a40-environment-build/environment_contract.yaml`

## Test Phases

### Phase 0: Safety and Ledger

1. Read the required standards and this test plan.
2. Confirm `commands.ps1` exists.
3. Register every terminal command in `commands.ps1` before execution.
4. Update `EXPERIMENT_LOG.md` after each meaningful sub-step.

### Phase 1: Static Contract Review

Verify that:
- GPU target remains NVIDIA A40.
- Docker base image is CUDA 12.1.1 + cuDNN8 + Ubuntu 22.04.
- Python target remains 3.10.
- PyTorch target remains 2.3.1 + cu121.
- Workspace and caches point to `/workspace`.
- Startup does not auto-run experiments.

### Phase 2: Dockerfile Build Check

Build target image as `linux/amd64`.

Suggested tag pattern:

```text
ghcr.io/pasavee123/cexar-a40:cuda121-torch231-<gitsha>
```

Do not use `latest` as the canonical experiment tag.

### Phase 3: Container Runtime Verification

Inside the built container, verify:

```text
python --version
nvcc --version
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available())"
python -c "import transformers, PIL, numpy, pandas, sklearn, psutil, tqdm, yaml; print('imports_ok')"
echo $HF_HOME
echo $TORCH_HOME
df -h /workspace
```

If run on an A40 host, also verify:

```text
nvidia-smi
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

Expected:
- Driver >= 550.xx on RunPod A40 host
- CUDA container: 12.1.x
- PyTorch: 2.3.1+cu121
- torch CUDA build: 12.1
- GPU: NVIDIA A40
- `/workspace` mounted and writable

### Phase 4: GHCR Readiness

Verify or document:
- Image is `linux/amd64`.
- GHCR tag is immutable or git-sha based.
- Public GHCR is preferred for first RunPod pull.
- Private GHCR requires RunPod Container Registry Auth with `read:packages`.

### Phase 5: Result

Write:
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:
- Any command was executed before being logged.
- The runner wants to change CUDA/PyTorch/Python/GPU target.
- Docker build requires unapproved credentials.
- GHCR push needs credentials not already approved by the human.
- SSH key, token, hostname, or PAT would be written into repo files.
- The image cannot be built or verified after 3 focused attempts.
