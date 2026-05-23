# RUNNER_INSTRUCTIONS.md

## Role

You are the runner. Execute only EXP-0014. Do not redesign the architecture.

## Mandatory Reading

Read before any command:

1. `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
2. `standards/runner_protocol.md`
3. `standards/experiment_protocol.md`
4. `standards/medical_claims_policy.md`
5. `standards/integration_gate.md`
6. `experiments/EXP-0012B-xrv-stratified-metric-fix/RESULT.md`
7. `experiments/EXP-0013-rad-dino-foundation-embedding-smoke/RESULT.md`
8. `experiments/EXP-0014-multimodel-contract-comparison/TEST_PLAN.md`

## Hard Boundary

This is a read-only artifact comparison.

Do not:

- install packages
- modify venvs
- run new model inference
- train
- classify RAD-DINO
- compute AUROC
- tune thresholds
- modify EXP-0012B artifacts
- modify EXP-0013 artifacts
- move/delete cleanup artifacts
- modify production code

## Commands

Use `commands.ps1` as the ledger.

Every command must be registered before execution.

Any copy/move/delete/cleanup command requires explicit approval and must be logged before execution. Prefer no cleanup in this experiment.

## Main Task

Create a small script:

```text
artifacts/run_contract_comparison.py
```

The script should read existing artifacts and write:

```text
artifacts/sample_alignment_report.json
artifacts/model_output_contract_comparison.json
artifacts/cexar_adapter_contract_draft.md
```

Use only standard library plus packages already available in the active environment if needed. Prefer Python standard library and `numpy` only if available.

## Final Result

Write `RESULT.md` with:

- artifact availability
- sample alignment status
- XRV output contract summary
- RAD-DINO output contract summary
- adapter contract recommendation
- limitations

No clinical claims.
