# RUNNER_INSTRUCTIONS.md

## Role

You are the runner for EXP-0015. Execute the test plan exactly. Do not redesign the experiment.

## Required Reading

Read these before doing any work:

1. `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
2. `standards/runner_protocol.md`
3. `standards/experiment_protocol.md`
4. `standards/medical_claims_policy.md`
5. `standards/integration_gate.md`
6. `experiments/EXP-0015-rad-dino-linear-probe-smoke-test/TEST_PLAN.md`
7. `experiments/EXP-0015-rad-dino-linear-probe-smoke-test/README.md`

## Execution Contract

Work only inside:

```text
experiments/EXP-0015-rad-dino-linear-probe-smoke-test/
```

Read-only inputs may come from:

```text
experiments/EXP-0012B-xrv-stratified-metric-fix/
experiments/EXP-0013-rad-dino-foundation-embedding-smoke/
experiments/EXP-0014-multimodel-contract-comparison/
```

Do not modify those prior experiment folders.

## Command Ledger Requirements

Before every terminal command, record the exact command in `commands.ps1`.

Do not write summaries such as:

- "multiple probes"
- "several commands"
- "checked artifacts"
- "ran script"

Each command must be exact and separate.

After each command or meaningful sub-step, update `EXPERIMENT_LOG.md`.

## Environment

Prefer:

```text
.venvs/cexar-foundation
```

Use it only if required packages already exist.

If `scikit-learn` is missing, stop and write `FAILURE_REPORT.md`. Do not install packages unless the human explicitly approves.

## Allowed Work

- Read CSV, JSON, and NPZ artifacts.
- Create a local script under this experiment's `artifacts/`.
- Produce validation, feasibility, split, and metric artifacts.
- Train a tiny fixed linear probe on precomputed embeddings only.

## Forbidden Work

- Do not run RAD-DINO inference.
- Do not fine-tune RAD-DINO.
- Do not train on full CheXpert.
- Do not perform hyperparameter search.
- Do not tune thresholds.
- Do not modify production code.
- Do not modify prior experiment artifacts.
- Do not make clinical claims.
- Do not delete, move, rename, or clean up files without explicit approval.

## Reporting

`RESULT.md` must clearly state that any metrics are pipeline sanity only.

If the run fails, write `FAILURE_REPORT.md` with the exact failed command, error, environment state, and next recommended action.

