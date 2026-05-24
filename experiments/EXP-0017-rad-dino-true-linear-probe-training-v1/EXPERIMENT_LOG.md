# EXPERIMENT_LOG.md

## 2026-05-24 16:25 - Phase 0: Safety & Ledger Setup

Read all preflight documents:
- experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md
- standards/runner_protocol.md
- standards/experiment_protocol.md
- standards/medical_claims_policy.md
- standards/integration_gate.md
- experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/EXP0017_READINESS.md
- experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/README.md
- experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/TEST_PLAN.md
- experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/RUNNER_INSTRUCTIONS.md

Experiment folder is in clean state. Skeleton files present, no prior run artifacts.

## 2026-05-24 16:26 - Phase 1: Environment Validation (CMD-001 through CMD-005)

CMD-001: Python version check
- Exit code: 0, Python 3.10.2

CMD-002: Package list
- Exit code: 0
- All required packages confirmed: torch 2.5.1, transformers 4.45.2, Pillow 12.2.0, numpy 1.26.4, pandas 2.2.2, scikit-learn 1.4.2, psutil 7.2.2

CMD-003: RAD-DINO local cache check
- Exit code: 0
- RAD-DINO weights found in local cache at ~/.cache/huggingface/hub/models--microsoft--rad-dino. No network download needed.

CMD-004: Manifest row count (first attempt - syntax error, retried)
CMD-004b: Manifest row count (corrected)
- Exit code: 0
- 1000 rows confirmed. 21 columns including all 11 CheXpert label columns.

CMD-005: PyTorch device check
- Exit code: 0
- PyTorch 2.5.1+cpu, CUDA not available, device=cpu.

Phase 1 PASSED. All requirements met.

## 2026-05-24 16:35 - Main Experiment Script Written

Wrote experiments/EXP-0017-rad-dino-true-linear-probe-training-v1/artifacts/run_exp0017_true_linear_probe.py (562 lines).
Fixed multiple f-string syntax errors (backslash-escaped quotes incompatible with Python 3.10).
Syntax verification: PASS.

## 2026-05-24 16:43 - CMD-006: Main Experiment Script Execution

Command: .venvs\cexar-foundation\Scripts\python.exe experiments\EXP-0017-rad-dino-true-linear-probe-training-v1\artifacts\run_exp0017_true_linear_probe.py
Working directory: D:\cexar-workbench
Exit code: 0

### Phase 1 Results (script-embedded)
- Manifest: 1000 rows, 11/11 labels present
- Weight source: local_cache
- Device: cpu
- Image spot-check: 0/20 missing
- Wrote: input_environment_validation.json

### Phase 2 Results: Corrected Split
- 982 unique patients
- Train: 688 patients (698 images), Val: 147 patients (152 images), Test: 147 patients (150 images)
- No patient overlap between splits
- U-zeros uncertain label policy applied
- 10/11 labels fully trainable (all splits have >=3 pos and >=3 neg)
- 1 label partially masked: Fracture (val_positive=1, below threshold 3)
- This is a significant improvement over the EXP-0016 random split which had 5 masked labels.
  - Previously masked but now trainable: Atelectasis, Pneumonia, Lung Lesion, Lung Opacity
- Wrote: corrected_split_manifest_1k.csv, corrected_split_report.json

### Phase 3 Results: RAD-DINO Embeddings
- Model: microsoft/rad-dino on cpu
- 1000/1000 images succeeded (100.0%), 0 failed
- Runtime: 1161.52s (~19.4 minutes)
- Embedding shape: [1000, 768]
- Throughput: ~0.86 images/second
- First embedding preview: [0.5325, 0.1766, 1.5697, -0.0090, 0.0410, -0.1974, 0.4986, -0.3611, -0.3311, -0.1631]
- CPU memory: before=84.6% used, total=15.63 GB
- Wrote: rad_dino_embeddings_1k.npz (compressed), rad_dino_embedding_summary_1k.json

### Phase 4 Results: Linear Probe Training
- Feature matrix: (1000, 768)
- All 11 probes trained (LogisticRegression, class_weight=balanced, max_iter=1000, solver=lbfgs, seed=42)
- Train AUROC: 1.0 on all labels (severe overfitting expected with 768 features on ~700 training samples)
- Test AUROC results (sorted by test AUROC):
  - Pneumothorax: 0.7887 (val: 0.7339)
  - Pleural Effusion: 0.6992 (val: 0.6956)
  - Edema: 0.6875 (val: 0.7406)
  - Cardiomegaly: 0.6806 (val: 0.7877)
  - Pneumonia: 0.6747 (val: 0.8002)
  - Lung Opacity: 0.6614 (val: 0.6278)
  - Lung Lesion: 0.6528 (val: 0.6952)
  - Enlarged Cardiomediastinum: 0.6438 (val: 0.3979)
  - Fracture: 0.5651 (val: NULL - masked, val_pos=1 < threshold 3)
  - Atelectasis: 0.5139 (val: 0.4202)
  - Consolidation: 0.4360 (val: 0.6267)
- Observed: Train AUROC=1.0 across all labels indicates severe overfitting. This is expected: 768 features for ~700 training samples with no regularization beyond balanced class weights.
- Wrote: linear_probe_metrics.json, linear_probe_model_inventory.json

### Phase 5 Results: Baseline Context Comparison
- Wrote: baseline_context_comparison.md
- Compares EXP-0017 against EXP-0013 (100-image smoke test) and EXP-0016 (dataset readiness check)

## 2026-05-24 17:03 - Experiment Completed

Overall status: PASS
Total runtime: ~19 minutes 24 seconds
All output artifacts generated successfully.
No production code, prior experiment artifacts, or dataset files modified.
