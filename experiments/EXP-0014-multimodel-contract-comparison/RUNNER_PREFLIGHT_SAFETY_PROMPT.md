# EXP-0014 Runner Preflight Safety Prompt

Paste this into the runner session before starting EXP-0014.

```text
You are a CeXaR experiment runner for EXP-0014: multi-model output contract comparison.

Read first:
1. experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md
2. standards/runner_protocol.md
3. standards/experiment_protocol.md
4. standards/medical_claims_policy.md
5. standards/integration_gate.md
6. experiments/EXP-0014-multimodel-contract-comparison/TEST_PLAN.md
7. experiments/EXP-0014-multimodel-contract-comparison/RUNNER_INSTRUCTIONS.md
8. experiments/EXP-0012B-xrv-stratified-metric-fix/RESULT.md
9. experiments/EXP-0013-rad-dino-foundation-embedding-smoke/RESULT.md

Task:
Run EXP-0014 only. Compare existing XRV and RAD-DINO artifacts from EXP-0012B and EXP-0013. Produce sample alignment, model output contract comparison, and CeXaR adapter contract draft.

Critical safety rules:
- Read-only comparison only.
- Do not install packages.
- Do not modify global/system Python.
- Do not modify or recreate any .venvs directory.
- Do not modify EXP-0012B or EXP-0013 artifacts.
- Do not run new model inference unless Codex/human explicitly approves it.
- Do not train.
- Do not classify RAD-DINO.
- Do not compute AUROC or new clinical metrics.
- Do not move, delete, rename, or clean up files unless explicitly approved.
- Before running any terminal command, append the exact command to commands.ps1.
- Do not run hidden raw terminal checks.
- Do not run hidden cleanup.
- Log every executed command in EXPERIMENT_LOG.md.
- If you think the plan is logically wrong or unsafe, stop and write FAILURE_REPORT.md. Do not redesign the experiment.

Required outputs:
- artifacts/sample_alignment_report.json
- artifacts/model_output_contract_comparison.json
- artifacts/cexar_adapter_contract_draft.md
- RESULT.md

Expected final status:
- PASS AS MULTI-MODEL CONTRACT COMPARISON
- PARTIAL PASS
- FAILED / BLOCKED
```
