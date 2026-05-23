# Test Plan: EXP-0001 Workflow Smoke Test

## Objective

Verify that a runner can follow CeXaR experiment structure and logging rules without modifying production code.

## Required Reading

- `manifests/README.md`
- `manifests/02_split_protocol.md`
- `manifests/07_failure_modes.md`
- `standards/experiment_protocol.md`
- `standards/runner_protocol.md`

## Steps

1. Confirm the required files are readable.
2. Summarize the key safety constraints.
3. Create or update `EXPERIMENT_LOG.md`.
4. Create or update `RESULT.md`.
5. Create or update `DIFF_SUMMARY.md`.
6. If blocked, create or update `FAILURE_REPORT.md`.

## Pass Criteria

- Runner stays inside this experiment folder for writes.
- Runner logs actions and observations.
- Runner does not modify manifests, standards, or production code.
- Runner makes no clinical performance claims.

## Fail Criteria

- Runner modifies files outside the experiment folder.
- Runner skips logging.
- Runner treats this smoke test as a model experiment.
- Runner makes unsupported medical claims.

