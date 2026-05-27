# TEST_PLAN.md

## Scope

EXP-0021 scales RAD-DINO embedding extraction from EXP-0020 from 100 images to 10,000 CheXpert images on RTX 6000 Ada.

Allowed:
- Author/update experiment-local scripts only.
- Run dry-run limits of 5 and 100 images.
- Run the approved 10,000-image embedding extraction after Codex review.
- Save large artifacts under `/workspace/exp_artifacts/EXP-0021`.
- Save lightweight summaries in this experiment folder.

Forbidden:
- No model training.
- No classifier/probe fitting.
- No AUROC/AUPRC or clinical metric calculation.
- No clinical claims.
- No production code edits.
- No dataset upload.
- No hidden cleanup/delete/move commands.
- No secrets, tokens, SSH keys, hostnames, private IPs, or API keys in repo files or logs.

## Required Inputs

- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/RESULT.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/configs/exp0021_config.yaml`
- `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv` as reference only

## Phase A: Script Authoring

DeepSeek may implement:

- `scripts/build_manifest_10k.py`
- `scripts/run_rad_dino_embedding_10k.py`
- `scripts/run_exp0021_10k.sh`

The scripts must support:

- deterministic manifest generation with a fixed seed
- deterministic path normalization
- `--limit` dry-run mode
- resumable embedding extraction
- sharded output `.npz` files
- summary JSON
- non-zero exit on zero successful images
- non-zero exit on embedding shape mismatch

After writing scripts, stop for Codex review before running the full 10k job.

## Phase B: Codex Script Review

Codex must verify:

- no destructive delete/cleanup behavior
- no package installation outside `/opt/venv`
- no production code edits
- no large artifact outputs inside git
- no clinical metric computation
- no hardcoded secrets
- correct RTX 6000 Ada runtime check
- correct path mapping from `D:\Dataset_Chexpert\archive` to `/workspace/chexpert_dataset_raw`
- resume/checkpoint behavior is understandable

## Phase C: Cloud Dry Run

Run:

```bash
bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 5 --dry-run-label dryrun5
bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 100 --dry-run-label dryrun100
```

Expected:

- RTX 6000 Ada detected
- CUDA available
- 5/5 then 100/100 image success
- embedding dimension 768
- artifacts written to `/workspace/exp_artifacts/EXP-0021`

## Phase D: 10k Run

Only after Phase B/C pass, run:

```bash
bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 10000
```

Expected:

- 10,000 images requested
- 10,000 images attempted unless stopped by documented failure
- all successful embeddings shape `[N, 768]`
- sharded outputs under `/workspace/exp_artifacts/EXP-0021/runs/full_10k/embeddings`
- lightweight summary copied into `artifacts/`

Observed on 2026-05-27:

- `images_attempted`: 10000
- `images_succeeded`: 10000
- `images_failed`: 0
- `embedding_dim`: 768
- `num_shards`: 10
- checkpoint `success_count`: 10000
- checkpoint completed index count: 10000
- external summary and git lightweight summary were byte-identical

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:

- GPU is not NVIDIA RTX 6000 Ada Generation.
- CUDA is unavailable.
- `/opt/venv` Python is unavailable.
- `/workspace/chexpert_dataset_raw` is unavailable.
- fewer than 10,000 candidate image paths can be resolved before the full run.
- dry-run 5 or 100 fails.
- image success count is zero.
- embedding dimension is not 768.
- a script would delete dataset/cache/repo files.
- exact command logging cannot be maintained.

