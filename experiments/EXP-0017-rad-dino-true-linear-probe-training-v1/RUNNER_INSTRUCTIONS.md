# RUNNER_INSTRUCTIONS.md

## Role

You are the runner for EXP-0017. This is the first controlled true downstream training experiment for RAD-DINO linear probes.

Execute the test plan exactly. Do not redesign the experiment.

## Required Reading

Read these before doing any work:

1. `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
2. `standards/runner_protocol.md`
3. `standards/experiment_protocol.md`
4. `standards/medical_claims_policy.md`
5. `standards/integration_gate.md`
6. `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/EXP0017_READINESS.md`
7. `experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/README.md`
8. `experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/TEST_PLAN.md`
9. `experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/RUNNER_INSTRUCTIONS.md`

## Work Area

Work only inside:

```text
experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/
```

Read-only inputs:

```text
experiments/EXP-0016-chexpert-scale-up-readiness/
experiments/EXP-0013-rad-dino-foundation-embedding-smoke/
D:\Dataset_Chexpert
```

Do not modify these input locations.

## Command Ledger Requirements

Before every terminal command, record the exact command in `commands.ps1`.

Do not write grouped summaries such as:

- "multiple checks"
- "ran training"
- "generated embeddings"
- "inspected results"

Each command must be exact and separate.

After each command or meaningful sub-step, update `EXPERIMENT_LOG.md`.

## Allowed Work

- Create corrected split artifacts.
- Generate RAD-DINO embeddings for the 1,000-image manifest.
- Train lightweight LogisticRegression probes on frozen embeddings.
- Compute research pipeline metrics only.
- Save artifacts inside this experiment folder.

## Forbidden Work

- Do not fine-tune RAD-DINO.
- Do not modify RAD-DINO weights.
- Do not modify `D:\Dataset_Chexpert`.
- Do not copy image files into this repository.
- Do not modify production code.
- Do not modify prior experiment artifacts.
- Do not tune clinical thresholds.
- Do not make clinical claims.
- Do not delete, move, rename, or clean up files without explicit approval.

## Dependency And Network Rules

Use `.venvs/cexar-foundation`.

If a required package is missing, stop and ask for human approval before installing.

If RAD-DINO weights are not available locally and network download is required, stop and ask for human approval before downloading.

## Reporting

All metric reports must include:

```text
RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE
```

If the experiment fails, write `FAILURE_REPORT.md` with exact failed command, error summary, files changed, environment state, and recommended next action.

