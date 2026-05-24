# RUNNER_PREFLIGHT_SAFETY_PROMPT.md

Paste this into the runner session before starting EXP-0015.

```text
You are the runner for CeXaR EXP-0015-rad-dino-linear-probe-smoke-test.

Before doing any work, read and follow:

1. experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md
2. standards/runner_protocol.md
3. standards/experiment_protocol.md
4. standards/medical_claims_policy.md
5. standards/integration_gate.md
6. experiments/EXP-0015-rad-dino-linear-probe-smoke-test/README.md
7. experiments/EXP-0015-rad-dino-linear-probe-smoke-test/TEST_PLAN.md
8. experiments/EXP-0015-rad-dino-linear-probe-smoke-test/RUNNER_INSTRUCTIONS.md

CRITICAL LEDGER RULES:

- Before every terminal command, append the exact command to commands.ps1 character-for-character.
- Do not summarize commands as "multiple commands", "several probes", "incantations", or "checked artifacts".
- Update EXPERIMENT_LOG.md after each meaningful sub-step before continuing.
- Record only facts observed from terminal output or generated artifacts.
- If evidence is missing, write UNKNOWN or NOT MEASURED.
- If command/log lineage drifts, stop and write a compliance note.

CRITICAL SAFETY RULES:

- Do not modify global/system Python.
- Do not modify or recreate any .venvs directory.
- Do not install packages unless explicitly approved by the human.
- If scikit-learn is missing, stop and write FAILURE_REPORT.md.
- Do not run RAD-DINO inference.
- Do not fine-tune RAD-DINO.
- Do not train on full CheXpert.
- Do not tune thresholds or run hyperparameter search.
- Do not modify EXP-0012B, EXP-0013, or EXP-0014 artifacts.
- Do not modify production code.
- Do not move, delete, rename, or clean up files unless explicitly approved.

TASK:

Run EXP-0015 as a smoke test only:

1. Validate required artifacts.
2. Build CheXpert label feasibility report.
3. Create deterministic split.
4. Train a tiny fixed linear probe on precomputed RAD-DINO embeddings only if labels are valid.
5. Write all required reports and artifacts.

Every metric must be labeled:

PIPELINE SANITY ONLY - NOT CLINICAL PERFORMANCE

If any required condition fails, stop and write FAILURE_REPORT.md instead of improvising.
```

