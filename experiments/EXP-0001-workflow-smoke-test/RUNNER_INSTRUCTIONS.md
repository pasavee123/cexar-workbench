# Runner Instructions: EXP-0001 Workflow Smoke Test

You are the runner, not the architect.

Follow `TEST_PLAN.md` exactly. Do not redesign the workflow.

## Allowed Write Scope

Only write inside:

`experiments/EXP-0001-workflow-smoke-test/`

## Forbidden Actions

- Do not edit `manifests/`
- Do not edit `standards/`
- Do not clone external repositories
- Do not install dependencies
- Do not train or evaluate models
- Do not modify production code

## Required Output

Update:

- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `DIFF_SUMMARY.md`

If blocked, update:

- `FAILURE_REPORT.md`

