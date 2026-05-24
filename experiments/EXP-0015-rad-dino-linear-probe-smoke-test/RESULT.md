# RESULT.md

## Experiment: EXP-0015 — RAD-DINO Linear Probe Smoke Test

### Result: PASS AS LINEAR PROBE SMOKE TEST

### Summary

The downstream linear-probe pipeline contract was validated end-to-end:

```text
sample_manifest.csv + rad_dino_embeddings.npz -> label matrix -> deterministic split -> lightweight probe -> sanity report
```

**PIPELINE SANITY ONLY — NOT CLINICAL PERFORMANCE**

### What Worked

- All required input artifacts were readable and validated: `sample_manifest.csv` (100 rows), `rad_dino_embeddings.npz` (shape [100, 768]), `rad_dino_embedding_summary.json` (100/100 succeeded).
- Embedding indices aligned with manifest indices [0..99].
- 9 of 11 CheXpert labels were usable for smoke training (both positive and negative examples present in the full sample).
- A deterministic patient-level split was created (seed=42, train=79, eval=21).
- 8 labels completed the smoke probe with AUROC computed on the eval set: Atelectasis (0.72), Consolidation (0.84), Edema (0.35), Pleural Effusion (0.70), Pneumonia (1.00), Cardiomegaly (0.50), Lung Opacity (0.70), Enlarged Cardiomediastinum (0.68).
- Invalid/skipped labels were documented with explicit reasons.

### What Did Not Work / Was Skipped

| Label | Reason |
|-------|--------|
| Lung Lesion | Zero positive examples in sample (0/100) |
| Fracture | Zero positive examples in sample (0/100) |
| Pneumothorax | All 2 positive examples landed in eval set after patient-level split; no positive in train |

### Pipeline Contract Status

| Component | Status |
|-----------|--------|
| Input validation | PASSED |
| Label feasibility | PASSED (9/11 usable) |
| Deterministic split | PASSED (patient-level, seed=42) |
| Probe training | PASSED (8 labels with AUROC) |
| Artifact traceability | PASSED |
| Command ledger integrity | PASSED |

### Pass/Fail Criteria Assessment

- Required artifacts are readable: PASS
- Embeddings align with manifest: PASS
- Label feasibility reported for all candidate labels: PASS
- Deterministic split recorded: PASS
- At least one label completed smoke probe without silent failure: PASS (8 labels)
- Invalid labels skipped with explicit reasons: PASS
- All commands exact in commands.ps1: PASS
- Every result traceable to command, log, or artifact: PASS
- No production code or prior experiment artifacts modified: PASS

### Medical Claims Notice

In this experiment, on the N=100 CheXpert validation sample with a deterministic patient-level split (seed=42), the LogisticRegression probe on frozen RAD-DINO embeddings produced per-label AUROC values in the range [0.35-1.00]. These values are pipeline sanity metrics only — they suggest the downstream probe path is technically viable but do not prove clinical usefulness. Key limitations include: N=100 sample with high variance, CPU-only computation, label noise in CheXpert validation set, class imbalance (e.g., Pneumonia with only 3 positive samples), and no external validation. Human-in-the-loop clinical validation is required before any clinical use.

### Required Follow-Up

- Larger-scale training on full CheXpert or MIMIC subsets
- GPU-based training to confirm performance scales
- Stratified sampling to ensure rare labels appear in train set
- External validation on held-out datasets
- Calibration and fairness evaluation