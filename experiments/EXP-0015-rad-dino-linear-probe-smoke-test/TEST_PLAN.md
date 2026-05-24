# TEST_PLAN.md

## Goal

Run a minimal, reproducible downstream linear-probe smoke test using precomputed RAD-DINO embeddings and CheXpert labels.

The goal is to validate the pipeline contract:

```text
sample_manifest.csv + rad_dino_embeddings.npz -> label matrix -> deterministic split -> lightweight probe -> sanity report
```

This experiment does not evaluate clinical performance.

## Non-Goals

- Do not run new RAD-DINO inference.
- Do not fine-tune RAD-DINO.
- Do not train a production model.
- Do not tune thresholds.
- Do not optimize hyperparameters beyond a tiny fixed smoke-test configuration.
- Do not modify EXP-0012B, EXP-0013, or EXP-0014 artifacts.
- Do not modify production code.

## Required Inputs

From EXP-0012B:

- `experiments/EXP-0012B-xrv-stratified-metric-fix/artifacts/sample_manifest.csv`

From EXP-0013:

- `experiments/EXP-0013-rad-dino-foundation-embedding-smoke/artifacts/rad_dino_embeddings.npz`
- `experiments/EXP-0013-rad-dino-foundation-embedding-smoke/artifacts/rad_dino_embedding_summary.json`

From EXP-0014:

- `experiments/EXP-0014-multimodel-contract-comparison/artifacts/model_output_contract_comparison.json`
- `experiments/EXP-0014-multimodel-contract-comparison/artifacts/cexar_adapter_contract_draft.md`

## Phase 0: Safety And Ledger

Before any command:

1. Read `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`.
2. Read `standards/runner_protocol.md`.
3. Read `standards/experiment_protocol.md`.
4. Read `standards/medical_claims_policy.md`.
5. Read `standards/integration_gate.md`.
6. Read this experiment's `RUNNER_INSTRUCTIONS.md`.
7. Read this experiment's `TEST_PLAN.md`.
8. Register every terminal command in `commands.ps1` exactly as executed.
9. Update `EXPERIMENT_LOG.md` after each meaningful sub-step.

Strict constraints:

- No global Python changes.
- No package installs unless already approved by the plan and logged exactly.
- Prefer the existing `.venvs/cexar-foundation` environment if it already has `numpy` and `scikit-learn`.
- If `scikit-learn` is missing, stop and write `FAILURE_REPORT.md` unless the human explicitly approves installation.
- No cleanup, move, rename, or delete commands without explicit human approval.

## Phase 1: Artifact Availability And Shape Check

Check that required inputs exist and are readable.

Verify:

- `sample_manifest.csv` has 100 rows.
- `rad_dino_embedding_summary.json` reports 100 attempted and 100 succeeded.
- `rad_dino_embeddings.npz` contains embeddings with shape `[100, 768]`.
- embedding indices, if present, align with manifest indices `[0..99]`.

Output:

```text
artifacts/input_validation_report.json
```

Stop if alignment fails.

## Phase 2: Label Matrix Construction

Construct a label matrix from CheXpert labels in `sample_manifest.csv`.

Rules:

- Use only labels present in the manifest.
- Treat positive label `1` as positive.
- Treat negative label `0` as negative.
- Treat uncertain, blank, missing, or non-numeric labels as missing unless the manifest contract explicitly says otherwise.
- Do not invent labels.

Report per label:

- positive count
- negative count
- missing count
- usable for smoke training: yes/no
- reason if skipped

Output:

```text
artifacts/label_feasibility_report.json
```

## Phase 3: Deterministic Split

Create a deterministic train/eval split for smoke testing.

Default:

- seed: `42`
- train fraction: `0.8`
- eval fraction: `0.2`

If patient identifiers are available and reliable, prefer patient-level separation. If not, record that patient-level leakage could not be fully assessed.

Output:

```text
artifacts/split_manifest.csv
```

Stop if no label has both positive and negative examples in both train and eval.

## Phase 4: Linear Probe Smoke Test

Train a tiny downstream probe on frozen embeddings only.

Allowed probe options:

- `sklearn.linear_model.LogisticRegression`
- a similarly simple linear classifier if already available

Fixed smoke-test configuration:

- deterministic seed: `42`
- max iterations: small fixed value such as `1000`
- no hyperparameter search
- no threshold tuning

For each usable label:

- train only on samples with non-missing label values
- require both positive and negative classes in train
- require both positive and negative classes in eval before computing AUROC
- if AUROC cannot be computed, skip and explain why

Output:

```text
artifacts/probe_smoke_metrics.json
```

Allowed metrics:

- AUROC for labels with both classes in eval
- class counts
- number of train/eval samples used

All metrics must be labeled:

```text
PIPELINE SANITY ONLY - NOT CLINICAL PERFORMANCE
```

## Phase 5: Summary And Review Package

Write:

- `RESULT.md`
- `DIFF_SUMMARY.md`
- `FAILURE_REPORT.md`
- `REVIEW_NOTES_FOR_CODEX.md`

`RESULT.md` must state one of:

- `PASS AS LINEAR PROBE SMOKE TEST`
- `PARTIAL PASS`
- `FAILED / BLOCKED`

## Pass Criteria

Pass if:

- Required artifacts are readable.
- Embeddings align with the manifest.
- Label feasibility is reported for all candidate labels.
- Deterministic split is recorded.
- At least one label completes the smoke probe without silent failure.
- Invalid labels are skipped with explicit reasons.
- All commands are exact in `commands.ps1`.
- Every result is traceable to command, log, or artifact.
- No production code or prior experiment artifacts are modified.

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:

- Required artifacts are missing.
- Embedding shape or indices do not align.
- No label is usable for smoke training.
- The environment lacks required packages and installation is not approved.
- The runner would need to rerun RAD-DINO inference.
- The runner would need to modify previous experiment artifacts.
- The runner detects command/log drift.
- The runner believes the plan is scientifically unsafe.

## Required Output Files

- `commands.ps1`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`
- `artifacts/input_validation_report.json`
- `artifacts/label_feasibility_report.json`
- `artifacts/split_manifest.csv`
- `artifacts/probe_smoke_metrics.json`
- `artifacts/run_rad_dino_linear_probe_smoke.py`

