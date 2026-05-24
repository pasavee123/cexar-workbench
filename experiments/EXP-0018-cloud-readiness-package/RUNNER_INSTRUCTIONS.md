# RUNNER_INSTRUCTIONS.md

## Role

You are the runner for EXP-0018. Your job is to prepare a cloud readiness package only.

Do not run cloud workloads.

## Required Reading

Read these before doing any work:

1. `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
2. `standards/runner_protocol.md`
3. `standards/experiment_protocol.md`
4. `standards/medical_claims_policy.md`
5. `standards/integration_gate.md`
6. `experiments/EXP-0018-cloud-readiness-package/README.md`
7. `experiments/EXP-0018-cloud-readiness-package/TEST_PLAN.md`
8. `experiments/EXP-0018-cloud-readiness-package/RUNNER_INSTRUCTIONS.md`

## Fixed GPU Target

The GPU target is fixed by the human:

```text
NVIDIA A40
```

Do not choose another GPU. If A40 is unavailable, write `FAILURE_REPORT.md` and stop.

## Allowed Work

- Create YAML, JSON, Markdown, shell template, and Python skeleton files.
- Read prior experiment artifacts.
- Estimate runtime and cost from prior local measurements.
- Define configs for future cloud runs.

## Forbidden Work

- Do not start cloud instances.
- Do not run SSH commands.
- Do not include credentials, tokens, API keys, hostnames, or private IPs.
- Do not upload dataset files.
- Do not run RAD-DINO inference.
- Do not train any model.
- Do not modify production code.
- Do not make clinical claims.

## Command Ledger

Every terminal command must be recorded exactly in `commands.ps1` before execution.

