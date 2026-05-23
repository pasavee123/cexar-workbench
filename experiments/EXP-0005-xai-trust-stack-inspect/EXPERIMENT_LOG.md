# EXPERIMENT_LOG.md

## Session 1 — XAI Trust Stack Inspection

### [2026-05-22 21:09] Steps 1-2: Install grad-cam and captum
- **WD:** `D:\cexar-workbench`
- **Command:** `pip install grad-cam captum` (first attempt with deps, timed out — tried upgrading torch)
- **Resolution:** `pip install captum grad-cam --no-deps` → success
- **Exit:** 0
- **Interpretation:** Both installed without triggering PyTorch upgrade.

### [2026-05-22 21:10] Step 3: Install ttach (grad-cam dependency)
- **WD:** `D:\cexar-workbench`
- **Command:** `pip install ttach --no-deps`
- **Exit:** 0

### [2026-05-22 21:11] Step 4: grad-cam smoke test (synthetic CNN)
- **WD:** `D:\cexar-workbench`
- **Exit:** 0
- **Stdout:** Output shape (1, 64, 64), values [0.0, 1.0], mean 0.107
- **Interpretation:** grad-cam works on simple CNN.

### [2026-05-22 21:11] Step 5: Captum IG smoke test (synthetic CNN)
- **WD:** `D:\cexar-workbench`
- **Exit:** 0
- **Stdout:** Attribution shape (1, 3, 64, 64), convergence delta -1.14e-5
- **Interpretation:** Captum IG works on simple CNN.

### [2026-05-22 21:12] Step 6: Install quantus
- **WD:** `D:\cexar-workbench`
- **Command:** `pip install quantus --no-deps`
- **Exit:** 0
- **Stdout:** Quantus 0.6.0 installed
- **Interpretation:** Available. Will need full install for runtime.

### [2026-05-22 21:12] Step 7: CheXlocalize repo inspection
- **WD:** `D:\cexar-workbench`
- **Command:** GitHub API
- **Exit:** 0
- **Stdout:** rajpurkarlab/cheXlocalize, MIT, 40 stars, updated 2026-05-22
- **Interpretation:** Active repo, MIT licensed.