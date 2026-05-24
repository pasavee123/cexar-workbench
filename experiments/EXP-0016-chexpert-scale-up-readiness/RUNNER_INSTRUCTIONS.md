# RUNNER_INSTRUCTIONS.md

## Role

You are the runner for EXP-0016. Execute the test plan exactly. Do not redesign the experiment.

## Required Reading

Read these before doing any work:

1. `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
2. `standards/runner_protocol.md`
3. `standards/experiment_protocol.md`
4. `standards/medical_claims_policy.md`
5. `standards/integration_gate.md`
6. `experiments/EXP-0016-chexpert-scale-up-readiness/README.md`
7. `experiments/EXP-0016-chexpert-scale-up-readiness/TEST_PLAN.md`
8. `experiments/EXP-0016-chexpert-scale-up-readiness/RUNNER_INSTRUCTIONS.md`

## Work Area

Work only inside:

```text
experiments/EXP-0016-chexpert-scale-up-readiness/
```

Read-only dataset root:

```text
D:\Dataset_Chexpert
```

Read-only prior experiment context:

```text
experiments/EXP-0012B-xrv-stratified-metric-fix/
experiments/EXP-0013-rad-dino-foundation-embedding-smoke/
experiments/EXP-0014-multimodel-contract-comparison/
experiments/EXP-0015-rad-dino-linear-probe-smoke-test/
```

Do not modify prior experiment folders or the dataset.

## Command Ledger Requirements

Before every terminal command, record the exact command in `commands.ps1`.

Do not write grouped summaries such as:

- "multiple checks"
- "several probes"
- "inspected dataset"
- "ran inventory"

Each command must be exact and separate.

After each command or meaningful sub-step, update `EXPERIMENT_LOG.md`.

## Environment

Prefer existing venv:

```text
.venvs/cexar-foundation
```

Allowed package use if already installed:

- Python standard library
- `numpy`
- `pandas` if already available
- `scikit-learn` if already available

If a needed package is missing, stop and ask for human approval before installing. Do not install automatically.

## Allowed Work

- Read CSV and metadata files.
- Check whether image paths exist.
- Create candidate CSV/JSON/Markdown artifacts in this experiment folder.
- Estimate runtime/storage based on observed prior experiment timing.

## Forbidden Work

- Do not modify `D:\Dataset_Chexpert`.
- Do not copy images into this repository.
- Do not run RAD-DINO inference.
- Do not generate embeddings at scale.
- Do not train a model.
- Do not fine-tune RAD-DINO.
- Do not calculate model performance metrics.
- Do not modify production code.
- Do not delete, move, rename, or clean up files without explicit approval.
- Do not make clinical claims.

## Reporting

`RESULT.md` must clearly say this is a scale-up readiness check only.

If the run fails, write `FAILURE_REPORT.md` with exact failed command, error summary, environment state, files changed, and recommended next action.

