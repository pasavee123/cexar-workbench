# TEST_PLAN.md

## Goal

Create a machine-readable cloud readiness package for EXP-0019 and EXP-0020.

EXP-0018 should produce:

- cloud provisioning config
- manifest integrity audit config/result stub
- regularized probe config
- 10-seed plan
- artifact path contract
- cloud runner Python skeletons
- SSH script templates
- cloud smoke readiness decision

## Required Inputs

- `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv`
- `experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/artifacts/linear_probe_metrics.json`
- `experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/artifacts/rad_dino_embedding_summary_1k.json`
- `experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/artifacts/corrected_split_report.json`

## Phase 0: Safety And Ledger

Before any command:

1. Read `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`.
2. Read `standards/runner_protocol.md`.
3. Read `standards/experiment_protocol.md`.
4. Read `standards/medical_claims_policy.md`.
5. Read `standards/integration_gate.md`.
6. Read this experiment's `RUNNER_INSTRUCTIONS.md`.
7. Read this experiment's `TEST_PLAN.md`.
8. Register every terminal command in `commands.ps1` exactly as executed.
9. Update `EXPERIMENT_LOG.md` after each meaningful sub-step.

## Phase 1: Cloud Provisioning Config

Create:

```text
cloud_provisioning_config.yaml
```

The GPU target must be fixed to NVIDIA A40. The runner may choose compatible software versions and disk/RAM recommendations, but may not choose another GPU.

## Phase 2: Manifest Integrity Audit

Create:

```text
manifest_integrity_audit.json
```

It must encode row count, required columns, label columns, patient ID policy, uncertain label policy, split policy, and image path policy.

## Phase 3: Regularized Probe Config

Create:

```text
configs/regularized_probe_config.yaml
configs/seed_plan.yaml
configs/artifact_paths.yaml
```

The plan must include 10 seeds, regularization search, and metric masking rules.

## Phase 4: Code Skeletons

Create skeleton Python modules under `src/`:

- `run_regularized_probe.py`
- `split_strategies.py`
- `embedding_io.py`
- `metrics.py`
- `manifest_audit.py`
- `cloud_runtime_check.py`

These files should be executable or importable skeletons with clear TODOs, but must not run training by default.

## Phase 5: SSH Script Templates

Create shell templates under `scripts/`:

- `ssh_cloud_smoke_template.sh`
- `setup_cloud_env.sh`
- `collect_artifacts.sh`

These must not contain credentials, private IPs, tokens, or user secrets.

## Phase 6: Estimates And Readiness

Create:

```text
cloud_cost_runtime_estimate.json
EXP0019_READINESS.json
```

`EXP0019_READINESS.json` must say whether the package is ready for cloud smoke execution and list blockers.

## Pass Criteria

Pass if:

- GPU target is fixed to A40.
- No credentials are included.
- No cloud commands are executed.
- Configs are machine-readable.
- Manifest audit requirements are explicit.
- Code skeletons are present.
- SSH templates are present but inert.
- All commands are exact in `commands.ps1`.

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:

- The runner tries to select a GPU other than A40.
- Required prior artifacts are missing.
- Secrets or credentials are required.
- The runner would need to run cloud/SSH commands.
- The runner detects command/log drift.

