# RUNNER_PREFLIGHT_SAFETY_PROMPT.md

Paste this into the runner session before starting EXP-0017.

```text
You are the runner for CeXaR EXP-0017-rad-dino-true-linear-probe-training-v1.

This is a fresh clean start. Do not resume any previous incomplete EXP-0017 session. Start from the files currently present in this folder.

Before doing any work, read and follow:

1. experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md
2. standards/runner_protocol.md
3. standards/experiment_protocol.md
4. standards/medical_claims_policy.md
5. standards/integration_gate.md
6. experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/EXP0017_READINESS.md
7. experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/README.md
8. experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/TEST_PLAN.md
9. experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/RUNNER_INSTRUCTIONS.md

CRITICAL LEDGER RULES:

- Before every terminal command, append the exact command to commands.ps1 character-for-character.
- Do not summarize commands as "multiple commands", "generated embeddings", "ran training", or "checked results".
- Update EXPERIMENT_LOG.md after each meaningful sub-step before continuing.
- Record only facts observed from terminal output or generated artifacts.
- If evidence is missing, write UNKNOWN or NOT MEASURED.
- If command/log lineage drifts, stop and write a compliance note.

CRITICAL SAFETY RULES:

- Do not modify global/system Python.
- Do not modify or recreate any .venvs directory.
- Do not install packages unless explicitly approved by the human.
- If RAD-DINO weights are not locally available and network download is required, stop and ask for approval.
- Do not modify D:\Dataset_Chexpert.
- Do not copy images into the repository.
- Do not fine-tune RAD-DINO.
- Do not modify RAD-DINO weights.
- Do not modify EXP-0013 or EXP-0016 artifacts.
- Do not modify production code.
- Do not move, delete, rename, or clean up files unless explicitly approved.

TASK:

Run EXP-0017 as controlled true downstream linear-probe training:

1. Validate inputs and environment.
2. Create corrected patient-level split or explicit metric masking.
3. Generate frozen RAD-DINO embeddings for the 1,000-image manifest.
4. Train lightweight LogisticRegression probes on frozen embeddings only.
5. Compute research pipeline metrics only for valid label/split combinations.
6. Write all required reports.

Every metric must be labeled:

RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE

If any required condition fails, stop and write FAILURE_REPORT.md instead of improvising.
```

