# REVIEW_NOTES_FOR_CODEX.md

## Experiment Result

**Status:** PASS AS RUNTIME AND RAD-DINO SMOKE

All pass/fail criteria met. No blocking failures.

## Key Items for Codex Review

### 1. Path Mapping Correction

The CheXpert dataset on the network volume has the structure:
```
/workspace/chexpert_dataset_raw/train/patientXXXXX/...
/workspace/chexpert_dataset_raw/valid/patientXXXXX/...
```

There is no `archive/` directory. The EXP-0016 manifest uses `D:\Dataset_Chexpert\archive\train\...` paths. The smoke script was invoked with `--windows-prefix "D:\Dataset_Chexpert\archive"` (including `archive` in the prefix) to correctly resolve paths.

**Recommendation:** Update `DATA_ASSET_MANIFEST.md` to clarify that the path mapping prefix may need to include `archive/` depending on the dataset layout. Consider making the `archive/` component configurable or adding a manifest-path-to-real-path normalization step.

### 2. Environment Variables

`HF_HOME` and `TORCH_HOME` are not pre-configured in the EXP-0019 image. They must be set at runtime to direct model/torch caches to `/workspace/.cache/...`.

**Recommendation:** Add these to the Dockerfile or to a shell profile in `/opt/venv/bin/activate`.

### 3. nvcc Missing

The CUDA compiler is not in the image. CUDA 12.1 runtime is available through PyTorch, but `nvcc` is absent. This is fine for inference-only experiments but may need addressing for any experiment requiring compilation.

### 4. Smoke Test Result

- 100/100 images processed successfully.
- Embedding shape: [100, 768] as expected.
- Runtime: 13.44 seconds on RTX 6000 Ada.
- VRAM peak: 750 MB reserved, 346.3 MB allocated.
- No training, classification, or clinical metrics were performed.

### 5. Branch Publishing

Runner is instructed to commit results to `exp/0020-runpod-smoke-result` (or a timestamped variant if the branch already exists). Codex should verify the branch contains only the EXP-0020 experiment folder changes.

### 6. No Clinical Claims

The result document includes an explicit medical claims statement confirming no clinical evaluation was performed. No AUROC, AUPRC, or diagnostic claims are present in any output.
