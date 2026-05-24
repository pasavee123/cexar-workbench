# REVIEW_NOTES_FOR_CODEX.md

## Experiment: EXP-0015 — RAD-DINO Linear Probe Smoke Test

### Result: PASS AS LINEAR PROBE SMOKE TEST

### Key Findings for Reviewer

1. **Pipeline contract validated.** The path `sample_manifest.csv + rad_dino_embeddings.npz -> label matrix -> split -> probe -> metrics` works end-to-end on the N=100 sample.

2. **Embedding alignment confirmed.** RAD-DINO embeddings (shape [100, 768]) align with manifest indices [0..99]. No drift or missing embeddings (100/100 succeeded per summary).

3. **Label quality.** All 11 CheXpert labels in the manifest have clean 0.0/1.0 values — no uncertain, missing, or non-numeric values. This is a characteristic of the specific deterministic random sample (seed=42) used by EXP-0012B.

4. **Rare labels are a known risk.** Two labels (Lung Lesion, Fracture) have zero positive examples in this 100-image sample. This matches findings from EXP-0012B and EXP-0014. Larger sample sizes or targeted oversampling would be needed.

5. **Patient-level split vulnerability.** Pneumothorax (2 positive examples total) was usable at the full-sample level but became untrainable after the patient-level split because both positives landed in eval. This is expected behavior for a 100-sample smoke test but highlights the need for stratified patient-level splitting at scale.

6. **Pneumonia AUROC=1.0 is a red flag.** With only 2 train positive and 1 eval positive example, a perfect AUROC is a small-sample artifact, not a meaningful signal. This label needs more data before any conclusions can be drawn.

7. **Edema AUROC=0.35 is below chance.** This could indicate that the RAD-DINO embeddings do not linearly separate Edema in this small split, or it could be a split artifact. Larger-scale evaluation needed.

### Items Requiring Human/Codex Decision

- Whether to proceed with larger-scale linear probe training on full CheXpert validation set
- Whether to replicate with GPU-based embeddings (current embeddings are CPU-only)
- Whether to add stratified patient-level splitting to ensure rare labels appear in train
- Whether the venv package installation (scikit-learn==1.4.2) should be persisted or noted in environment docs

### Risk Flags

| Risk | Severity | Notes |
|------|----------|-------|
| Small sample variance | HIGH | N=100; AUROC values are unstable |
| Rare label absence | MEDIUM | Lung Lesion and Fracture have no positives |
| Patient-level split leakage | LOW | Patient-level split verified; 99 unique patients |
| Pneumonia perfect AUROC | LOW | Known artifact of 3 total positive examples |
| No external validation | HIGH | Standard limitation for all CeXaR experiments |
| CPU-only embeddings | LOW | Embeddings may differ from GPU-computed embeddings |

### Artifact Traceability

All results are traceable to:
- `commands.ps1` — CMD-001 through CMD-005
- `EXPERIMENT_LOG.md` — full chronological log
- `artifacts/input_validation_report.json` — Phase 1 output
- `artifacts/label_feasibility_report.json` — Phase 2 output
- `artifacts/split_manifest.csv` — Phase 3 output
- `artifacts/probe_smoke_metrics.json` — Phase 4 output
- `artifacts/run_rad_dino_linear_probe_smoke.py` — Reproducible source script

### Wrong-Path Incident

The first script execution wrote `input_validation_report.json` to a nested wrong path (inside `experiments/EXP-0015-.../experiments/EXP-0015-.../artifacts/`) due to a BASE path resolution bug. This was corrected in the same session (4 dirnames needed instead of 2). The wrong-path file has NOT been deleted. Please approve cleanup or leave as evidence of the bug.

### Compliance Backfill Note

During Codex review, a command ledger gap was found.

`EXPERIMENT_LOG.md` reported two failed script attempts before the successful run:

1. Attempt 1 failed because a relative venv path was not found from the experiment directory.
2. Attempt 2 failed because the script used incorrect BASE path resolution.

These failed attempts were not recorded as separate exact commands in `commands.ps1` at execution time. Because the exact terminal text cannot be verified from the current artifacts, the backfilled entries in `commands.ps1` are explicitly marked as `UNKNOWN - NOT RECORDED AT EXECUTION TIME`.

This is a compliance limitation, not a model-result failure. The final successful run remains traceable through CMD-004 and the generated artifacts.

### Nested Wrong-Path Artifacts

Two wrong-path artifact locations were found during Codex review:

1. `D:\cexar-workbench\experiments\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`
2. `D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`

These files appear to be leftover `input_validation_report.json` outputs from failed BASE path resolution attempts.

Cleanup status:

- Not deleted.
- Not moved.
- Preserved as evidence.
- Human approval is required before any cleanup command is run.

The correct artifact is:

`D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`