# EXPERIMENT_LOG.md

## Run Date: 2026-05-24

---

### Phase 0: Safety and Ledger (Setup)

**Timestamp:** 2026-05-24T13:37 UTC+7
**Action:** Read all required protocol files:
- `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0016-chexpert-scale-up-readiness/README.md`
- `experiments/EXP-0016-chexpert-scale-up-readiness/TEST_PLAN.md`
- `experiments/EXP-0016-chexpert-scale-up-readiness/RUNNER_INSTRUCTIONS.md`
**Outcome:** All protocols read. No conflicts detected.

**Timestamp:** 2026-05-24T13:37 UTC+7
**Action:** Inspected experiment folder structure.
**Outcome:** Folder exists with template files. `artifacts/` directory exists with `.gitkeep` only. `commands.ps1` has header only. `EXPERIMENT_LOG.md` is empty template.

**Timestamp:** 2026-05-24T13:37 UTC+7
**Command:** CMD-001 - Listed dataset root structure (Get-ChildItem -Recurse -Depth 2 D:\Dataset_Chexpert)
**Exit Code:** 0
**Summary:** Dataset at `D:\Dataset_Chexpert\archive\` contains:
- `train/` directory with patient subdirectories (patient00001 through ~patient64540+)
- `valid/` directory with patient subdirectories (patient64541 through ~patient64740+)
- `train.csv` and `valid.csv`
**Files Created:** None

**Timestamp:** 2026-05-24T13:37 UTC+7
**Command:** CMD-002 - Checked venv Python and package versions
**Exit Code:** 0
**Summary:** Python 3.10.2. numpy 1.26.4 installed. sklearn 1.4.2 installed. **pandas NOT installed.**
**Files Created:** None

**Timestamp:** 2026-05-24T13:38 UTC+7
**Action:** Paused execution. Asked human for approval to install pandas into .venvs/cexar-foundation.
**Outcome:** Human approved pandas==2.2.2 installation with specific rules.

**Timestamp:** 2026-05-24T13:38 UTC+7
**Command:** CMD-003 - Installed pandas into existing venv (.venvs/cexar-foundation)
**Exit Code:** 0
**Summary:** pandas==2.2.2 installed successfully along with dependencies (python-dateutil, pytz, tzdata, six).
**Files Modified:** .venvs/cexar-foundation/Lib/site-packages/ (new packages added)

**Timestamp:** 2026-05-24T13:38 UTC+7
**Command:** CMD-004 - Verified pandas installation
**Exit Code:** 0
**Summary:** pandas 2.2.2 confirmed.
**Files Created:** None

---

### Phase 1: Dataset Inventory

**Timestamp:** 2026-05-24T13:38 UTC+7
**Command:** CMD-005 - Inspected train.csv structure
**Exit Code:** 0
**Summary:** 223,414 rows, 19 columns. Columns: Path, Sex, Age, Frontal/Lateral, AP/PA, No Finding, and 13 label/observation columns including all 11 CheXpert labels. Path format: `CheXpert-v1.0-small/train/patientXXXXX/studyN/viewN_frontal.jpg`

**Timestamp:** 2026-05-24T13:38 UTC+7
**Command:** CMD-006 - Inspected valid.csv structure
**Exit Code:** 0
**Summary:** 234 rows, same 19 columns as train.csv.

**Timestamp:** 2026-05-24T13:40 UTC+7
**Command:** CMD-008 - Ran full analysis script (run_chexpert_scale_up_readiness.py)
**Exit Code:** 0
**Summary Phase 1:** Dataset inventory confirmed:
- Train: 223,414 rows, 64,540 unique patients, all 223,414 image paths resolve to existing files (0 missing)
- Valid: 234 rows, 200 unique patients
- 191,027 frontal / 32,387 lateral images in train
- No patient overlap between train and valid
- Patient IDs extracted from directory name pattern in Path column
**Files Created:** artifacts/dataset_inventory_report.json

---

### Phase 2: Candidate Manifest Creation

**Timestamp:** 2026-05-24T13:40 UTC+7
**Command:** CMD-008 (continued)
**Summary Phase 2:**
- Combined pool: 223,648 valid rows with existing images
- Frontal pool: 191,229; Non-frontal pool: 32,419
- Selected 1,000 images, all frontal (deterministic seed 42)
- Manifest includes: sample_index, resolved_path, patient_id, source_csv, csv_row_idx, Frontal/Lateral, Sex, Age, AP/PA, all 11 CheXpert labels, split_placeholder
**Files Created:** artifacts/candidate_manifest_1k.csv

---

### Phase 3: Label Distribution

**Timestamp:** 2026-05-24T13:40 UTC+7
**Command:** CMD-008 (continued)
**Summary Phase 3:** Per-label distribution for 1k manifest:

| Label | Positive | Negative | Uncertain | Missing | Usable |
|-------|----------|----------|-----------|---------|--------|
| Atelectasis | 163 | 7 | 163 | 667 | Yes |
| Consolidation | 67 | 138 | 119 | 676 | Yes |
| Pneumothorax | 95 | 255 | 15 | 635 | Yes |
| Edema | 266 | 75 | 67 | 592 | Yes |
| Pleural Effusion | 388 | 145 | 46 | 421 | Yes |
| Pneumonia | 32 | 10 | 85 | 873 | Yes |
| Cardiomegaly | 133 | 41 | 36 | 790 | Yes |
| Lung Lesion | 44 | 6 | 2 | 948 | Yes |
| Fracture | 37 | 11 | 4 | 948 | Yes |
| Lung Opacity | 483 | 24 | 28 | 465 | Yes |
| Enlarged Cardiomediastinum | 55 | 89 | 62 | 794 | Yes |

All 11 labels have usable positive and negative samples. Uncertain labels (-1.0) are reported separately. Recommendation: U-zeros policy (standard CheXpert) for uncertain labels, pending Codex/human decision.
**Files Created:** artifacts/label_distribution_report.json

---

### Phase 4: Patient-Level Split Feasibility

**Timestamp:** 2026-05-24T13:40 UTC+7
**Command:** CMD-008 (continued)
**Summary Phase 4:**
- Patient IDs available: Yes (extracted from path)
- 982 unique patients in the 1k manifest
- Split: train=687 patients, validation=147, test=148
- Split ratio: 70/15/15, seed 42
- No patient overlap across splits
- All labels have positive samples in all three splits with the default random split; labels with very low positive counts (Lung Lesion, Fracture, Pneumonia) may benefit from stratified sampling in full-scale EXP-0017.
**Files Created:** artifacts/patient_split_feasibility_report.json, artifacts/candidate_split_manifest_1k.csv

---

### Phase 5: Runtime and Storage Estimate

**Timestamp:** 2026-05-24T13:40 UTC+7
**Command:** CMD-008 (continued)
**Summary Phase 5:**
Based on EXP-0013 reference (100 images, 90.35s CPU, shape [100, 768]):
- 1,000 images: 2.93 MB, ~15.1 min CPU
- 5,000 images: 14.65 MB, ~75.3 min CPU
- 10,000 images: 29.30 MB, ~150.6 min CPU
- Full dataset (223k+): ~50+ hours CPU, GPU strongly recommended
- Disk space requirement is minimal (< 1 GB even for full dataset)
- RAM requirement is negligible (embedding matrix ~700 MB for full dataset)
**Files Created:** artifacts/scale_up_runtime_estimate.md

---

### Phase 6: EXP-0017 Readiness Decision

**Timestamp:** 2026-05-24T13:40 UTC+7
**Command:** CMD-008 (continued)
**Summary Phase 6:**
- All 11 CheXpert labels confirmed usable for training
- No blockers identified: all image paths resolve, no patient overlap, all labels have positive/negative samples
- Recommended starting size: 1,000 images
- Recommended split: patient-level 70/15/15 with seed 42
- New RAD-DINO embeddings should be generated
- GPU optional for 1k, recommended for larger scales
- Uncertain label policy (U-zeros recommended) requires Codex/human decision
**Files Created:** artifacts/EXP0017_READINESS.md

---

### Final Status

**Completion:** All 6 phases executed successfully.
**Result:** PARTIAL PASS AS SCALE-UP READINESS CHECK (corrected per Codex review)
**Total Commands:** 9 commands registered in commands.ps1 (CMD-001 through CMD-009)
**Artifacts:** 9 files in artifacts/

---

## Correction Pass (Codex Review)

**Timestamp:** 2026-05-24T14:11 UTC+7
**Action:** Codex review triggered correction pass.
**What Codex found:**
1. `patient_split_feasibility_report.json` marked all labels as sufficiently represented, but the `needs_stratified_sampling` check only examined positive counts with a threshold of <3.
2. Three labels had zero negatives in validation or test: Atelectasis (test_neg=0), Pneumonia (val_neg=0), Lung Lesion (val_neg=0, test_neg=0).
3. Two additional labels had negatives below the threshold in validation or test: Fracture (val_neg=1, test_neg=2), Lung Opacity (val_neg=2).
4. EXP0017_READINESS.md, RESULT.md, FAILURE_REPORT.md, and REVIEW_NOTES_FOR_CODEX.md overstated readiness.
5. commands.ps1 CMD-007 was missing the exact failed inline command text.

**Files corrected:**
- `artifacts/run_chexpert_scale_up_readiness.py` - Fixed phase4_patient_split logic and phase6 result
- `artifacts/patient_split_feasibility_report.json` - Regenerated with corrected split feasibility checks
- `artifacts/EXP0017_READINESS.md` - Regenerated with PARTIAL PASS result and split correction requirements
- `RESULT.md` - Updated to PARTIAL PASS AS SCALE-UP READINESS CHECK
- `FAILURE_REPORT.md` - Added Codex Review Correction section
- `DIFF_SUMMARY.md` - Updated with correction details
- `REVIEW_NOTES_FOR_CODEX.md` - Updated with correction confirmation and split detail table
- `EXPERIMENT_LOG.md` - This section appended
- `commands.ps1` - Added CMD-009 (correction re-run) and AUDIT-BACKFILL-001 (unrecoverable CMD-007 text)

**Confirmation:** No training, RAD-DINO inference, embedding generation, dataset modification, cleanup, or package installation occurred during the correction pass. No prior experiment artifacts were modified.