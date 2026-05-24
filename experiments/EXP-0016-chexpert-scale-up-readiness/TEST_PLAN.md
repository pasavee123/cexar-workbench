# TEST_PLAN.md

## Goal

Assess whether the local CheXpert dataset is ready for larger-scale RAD-DINO downstream training.

The intended path is:

```text
dataset inventory -> candidate manifest -> label distribution -> patient-level split feasibility -> runtime/storage estimate -> EXP-0017 readiness decision
```

This experiment does not train a model.

## Non-Goals

- Do not train a classifier.
- Do not run RAD-DINO inference or generate embeddings at scale.
- Do not fine-tune RAD-DINO.
- Do not compute model performance metrics.
- Do not tune thresholds.
- Do not modify dataset files.
- Do not copy image files into this repo.
- Do not modify production code.

## Required Inputs

- Local dataset root: `D:\Dataset_Chexpert`
- Existing project context from EXP-0012B, EXP-0013, EXP-0014, and EXP-0015.

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
- Prefer existing `.venvs/cexar-foundation` only for read-only CSV/path analysis if needed.
- No cleanup, move, rename, or delete commands without explicit human approval.
- Do not modify `D:\Dataset_Chexpert`.

## Phase 1: Dataset Inventory

Inspect `D:\Dataset_Chexpert` and identify:

- CSV files
- likely training/validation label files
- image root directories
- number of rows in available CSVs
- available columns
- path column names
- patient identifier source

Output:

```text
artifacts/dataset_inventory_report.json
```

Stop if no usable dataset CSV or image-path column can be identified.

## Phase 2: Candidate Manifest Creation

Create deterministic candidate manifests for future experiments.

Minimum required:

```text
artifacts/candidate_manifest_1k.csv
```

Optional if fast and safe:

```text
artifacts/candidate_manifest_5k.csv
```

Rules:

- Use deterministic seed `42`.
- Prefer frontal chest X-ray images if view information is available.
- Include only rows with existing image paths after path resolution.
- Do not copy image files.
- Include enough columns to reproduce sample selection:
  - `sample_index`
  - source CSV row index
  - resolved image path
  - patient ID if available
  - split placeholder if later computed
  - selected CheXpert labels

If fewer than 1,000 valid rows exist, create the largest possible manifest and explain why.

## Phase 3: Label Distribution

For candidate manifest(s), report per-label distribution for the 11 CheXpert labels used in prior experiments:

- Atelectasis
- Consolidation
- Pneumothorax
- Edema
- Pleural Effusion
- Pneumonia
- Cardiomegaly
- Lung Lesion
- Fracture
- Lung Opacity
- Enlarged Cardiomediastinum

Report:

- positive count
- negative count
- uncertain count
- missing count
- usable for training: yes/no
- reason if not usable

Output:

```text
artifacts/label_distribution_report.json
```

Do not invent uncertain-label policy. If uncertain labels exist, report them and recommend a policy for Codex/human approval.

## Phase 4: Patient-Level Split Feasibility

Attempt a deterministic patient-level split plan.

Default target:

- train: 70%
- validation: 15%
- test: 15%
- seed: 42

Requirements:

- No patient ID should appear in more than one split if patient IDs are available.
- Report whether each label has positive and negative samples in each split.
- Report labels that require stratified or targeted sampling.

Output:

```text
artifacts/patient_split_feasibility_report.json
artifacts/candidate_split_manifest_1k.csv
```

If patient-level split is impossible because patient IDs are unavailable, do not improvise silently. Report the limitation and propose next steps.

## Phase 5: Runtime And Storage Estimate

Estimate resources for EXP-0017 embedding generation and training.

Use observed EXP-0013 timing as reference:

- 100 images
- CPU i7-12700H
- RAD-DINO embeddings shape `[100, 768]`
- runtime approximately 90.35 seconds

Estimate for:

- 1,000 images
- 5,000 images
- 10,000 images if dataset size supports it

Report:

- expected embedding file size
- expected runtime on CPU
- whether GPU should be required for practical training
- risks around disk, RAM, and wall-clock time

Output:

```text
artifacts/scale_up_runtime_estimate.md
```

## Phase 6: EXP-0017 Readiness Decision

Write:

```text
artifacts/EXP0017_READINESS.md
```

It must include:

- Recommended sample size for EXP-0017
- Recommended labels for first true linear-probe training
- Labels to skip or oversample
- Recommended split policy
- Whether new RAD-DINO embeddings should be generated
- Whether GPU is recommended
- Remaining blockers

## Final Reports

Write or update:

- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`

`RESULT.md` must state one of:

- `PASS AS SCALE-UP READINESS CHECK`
- `PARTIAL PASS`
- `FAILED / BLOCKED`

## Pass Criteria

Pass if:

- Dataset root exists and is readable.
- At least one usable dataset CSV is identified.
- Candidate manifest is created deterministically.
- Existing image-path rate is measured.
- Label distribution is reported.
- Patient-level split feasibility is reported.
- Runtime/storage estimate is written.
- EXP-0017 readiness recommendation is written.
- All commands are exact in `commands.ps1`.
- No dataset, production code, or prior experiment artifacts are modified.

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:

- Dataset root is missing or unreadable.
- No usable CSV can be identified.
- No usable image paths can be resolved.
- The runner would need to install packages without human approval.
- The runner would need to modify dataset files.
- The runner detects command/log drift.
- The runner believes the planned split or label policy is scientifically unsafe.

## Required Output Files

- `commands.ps1`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`
- `artifacts/dataset_inventory_report.json`
- `artifacts/candidate_manifest_1k.csv`
- `artifacts/label_distribution_report.json`
- `artifacts/patient_split_feasibility_report.json`
- `artifacts/candidate_split_manifest_1k.csv`
- `artifacts/scale_up_runtime_estimate.md`
- `artifacts/EXP0017_READINESS.md`
- `artifacts/run_chexpert_scale_up_readiness.py`

