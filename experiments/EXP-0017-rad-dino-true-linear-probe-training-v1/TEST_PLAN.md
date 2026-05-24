# TEST_PLAN.md

## Goal

Run the first true downstream RAD-DINO linear-probe training experiment on a deterministic 1,000-image CheXpert manifest.

Pipeline:

```text
EXP-0016 candidate_manifest_1k.csv
-> corrected patient-level split
-> RAD-DINO frozen embeddings [1000, 768]
-> lightweight per-label probes
-> research pipeline metrics and review report
```

This experiment is not clinical validation.

## Non-Goals

- Do not fine-tune RAD-DINO.
- Do not train a production model.
- Do not modify production code.
- Do not modify `D:\Dataset_Chexpert`.
- Do not copy image files into the repository.
- Do not tune thresholds for clinical use.
- Do not make clinical claims.

## Required Inputs

From EXP-0016:

- `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv`
- `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/patient_split_feasibility_report.json`
- `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/EXP0017_READINESS.md`

Environment:

- `.venvs/cexar-foundation`
- RAD-DINO local cache if available

Dataset:

- `D:\Dataset_Chexpert`

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
- No package installs unless explicitly approved by the human.
- Use only `.venvs/cexar-foundation` unless Codex/human approves otherwise.
- No cleanup, move, rename, or delete commands without explicit human approval.
- Do not modify prior experiment artifacts.
- Do not modify `D:\Dataset_Chexpert`.

## Phase 1: Input And Environment Validation

Verify:

- candidate manifest exists and has exactly 1,000 rows.
- all image paths exist.
- patient IDs are present.
- all 11 CheXpert label columns are present.
- `torch`, `transformers`, `Pillow`, `numpy`, `pandas`, and `scikit-learn` are available.
- device is recorded as CPU or CUDA.
- RAD-DINO weights are locally available, or the runner stops to request download approval.

Output:

```text
artifacts/input_environment_validation.json
```

## Phase 2: Corrected Patient-Level Split

Create a corrected patient-level split from EXP-0016 `candidate_manifest_1k.csv`.

Requirements:

- Seed: `42`
- Target split ratio: train 70%, validation 15%, test 15%
- No patient ID appears in more than one split.
- Default uncertain-label policy: `U-zeros` (`-1.0 -> 0.0`)
- For metric-reported labels, train/validation/test must each contain both positive and negative samples.
- If a label cannot satisfy both-class requirements, it must be explicitly masked from affected metrics.

Core labels that should be preserved if possible:

- Consolidation
- Pneumothorax
- Edema
- Pleural Effusion
- Cardiomegaly
- Enlarged Cardiomediastinum

Outputs:

```text
artifacts/corrected_split_manifest_1k.csv
artifacts/corrected_split_report.json
```

## Phase 3: RAD-DINO Embedding Generation

Generate frozen RAD-DINO embeddings for the 1,000-image corrected split manifest.

Rules:

- Use RAD-DINO frozen encoder only.
- Do not fine-tune or train RAD-DINO.
- Save embeddings inside this experiment only.
- Record runtime and memory/VRAM if measurable.
- Prefer local cache.
- If network/model download is required, stop and ask for human approval.

Outputs:

```text
artifacts/rad_dino_embeddings_1k.npz
artifacts/rad_dino_embedding_summary_1k.json
```

Stop if fewer than 95% of images succeed.

## Phase 4: Linear Probe Training

Train lightweight downstream probes on frozen embeddings.

Allowed model:

- `sklearn.linear_model.LogisticRegression`

Fixed config:

- seed `42`
- `class_weight="balanced"`
- `max_iter=1000`
- solver `lbfgs` or documented fallback

Rules:

- Train one binary probe per label.
- Use only train split for fitting.
- Use validation split for reporting and sanity checks.
- Use test split once for final research pipeline reporting.
- No hyperparameter search.
- No threshold tuning.
- Skip metrics when the relevant split lacks both classes.

Metrics:

- AUROC where valid
- AUPRC where valid
- class counts for train/validation/test

Outputs:

```text
artifacts/linear_probe_metrics.json
artifacts/linear_probe_model_inventory.json
```

Model files are optional. If saved, they must be inside `artifacts/models/` and marked experimental.

## Phase 5: Baseline Context Comparison

Compare cautiously against prior experiments only as pipeline context.

Allowed:

- compare sample size
- compare label coverage
- compare pipeline readiness
- compare rough sanity metrics with strong warnings

Forbidden:

- claiming clinical superiority
- treating N=1,000 as external validation
- production readiness claims

Output:

```text
artifacts/baseline_context_comparison.md
```

## Phase 6: Final Reports

Write:

- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`

`RESULT.md` must state one of:

- `PASS AS TRUE LINEAR PROBE TRAINING V1`
- `PARTIAL PASS`
- `FAILED / BLOCKED`

Every metric section must include:

```text
RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE
```

## Pass Criteria

Pass if:

- Input manifest is valid.
- Corrected patient-level split is produced or metric masking is honestly documented.
- RAD-DINO embeddings are generated for at least 95% of images.
- At least one label trains successfully.
- Metrics are computed only for valid labels/splits.
- All commands are exact in `commands.ps1`.
- No production code, prior experiment artifacts, or dataset files are modified.
- No clinical claims are made.

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:

- Required input artifacts are missing.
- Dataset images cannot be read.
- Dependencies are missing and installation is not approved.
- RAD-DINO weights are unavailable and download is not approved.
- More than 5% of embedding generation fails.
- No label can be trained safely.
- The runner detects command/log drift.
- The runner believes split policy, label policy, or metric reporting is scientifically unsafe.

## Required Output Files

- `commands.ps1`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`
- `artifacts/input_environment_validation.json`
- `artifacts/corrected_split_manifest_1k.csv`
- `artifacts/corrected_split_report.json`
- `artifacts/rad_dino_embeddings_1k.npz`
- `artifacts/rad_dino_embedding_summary_1k.json`
- `artifacts/linear_probe_metrics.json`
- `artifacts/linear_probe_model_inventory.json`
- `artifacts/baseline_context_comparison.md`
- `artifacts/run_exp0017_true_linear_probe.py`

