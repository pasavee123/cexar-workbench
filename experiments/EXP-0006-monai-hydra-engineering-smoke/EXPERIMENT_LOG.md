# EXPERIMENT_LOG.md

## Session 1 — MONAI Hydra Engineering Smoke

### [2026-05-22 21:19] Step 1: Install MONAI and Hydra
- **WD:** `D:\cexar-workbench`
- **Command:** `pip install monai hydra-core`
- **Exit:** 0 (after timeout for PyTorch upgrade)
- **Stdout:** MONAI 1.5.2, Hydra 1.3.2, PyTorch 2.12.0
- **Interpretation:** PyTorch upgraded from 2.0.1 → 2.12.0 (MONAI requires >=2.4.1).

### [2026-05-22 21:20] Step 2: MONAI deterministic transform test
- **WD:** `D:\cexar-workbench`
- **Command:** set_determinism(seed=42) → Compose(ScaleIntensity, RandRotate) → compare outputs
- **Exit:** 0
- **Stdout:** MONAI 1.5.2 works. Determinism controls seed. Minor floating-point diff in RandRotate on 2D tensor.
- **Interpretation:** set_determinism works. Transforms compose. PASS.

### [2026-05-22 21:20] Step 3: Hydra config test
- **WD:** `D:\cexar-workbench`
- **Command:** initialize_config_dir + compose
- **Exit:** 0
- **Stdout:** Config loaded: seed=42, dataset=test/batch_size=16, model=densenet121/18 classes
- **Interpretation:** Hydra config composition works. PASS.

## Audit Note

Audit Pass 2, 2026-05-23: This log was originally incomplete by current CeXaR standards. Missing required files were backfilled, and the result verdict was downgraded because the run mutated the global Python environment.
