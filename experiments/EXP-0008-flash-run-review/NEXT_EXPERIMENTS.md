# Next Experiments

Only 3 experiments recommended. All increase reliability without broad uncontrolled installation.

---

## EXP-0009: Environment Isolation & Lockfile Plan

### Hypothesis
CeXaR can have a reproducible, version-pinned environment that isolates PyTorch 2.0.1 (production) from PyTorch 2.4+ (RAD-DINO/MONAI experiments) via separate venvs or conda envs, preventing the global upgrade contamination observed in EXP-0006.

### Why It Matters
EXP-0006's global PyTorch upgrade from 2.0.1 to 2.12.0 broke reproducibility across all experiments. No further install-heavy experiment is safe until the environment is compartmentalized. This is the highest-priority blocker.

### Allowed Actions
- Create `experiments/EXP-0009-env-isolation/` folder.
- Inspect the current global pip list as-is (do not modify).
- Create a `requirements.in` or `pyproject.toml` with pinned versions for each experiment tier:
  - **Tier 1 (baseline)**: torch==2.0.1, torchvision==0.15.2, torchxrayvision==1.4.0
  - **Tier 2 (foundation)**: transformers>=4.30,<=4.40, open_clip_torch==3.3.0, timm==0.4.12
  - **Tier 3 (XAI)**: grad-cam==1.5.5, captum==0.9.0, quantus==0.6.0 (with full deps)
  - **Tier 4 (engineering)**: monai==1.5.2, hydra-core==1.3.2, torch>=2.4 (isolated env)
- Write a `lockfile_plan.md` describing: venv creation commands, activation, and which experiments belong to which tier.
- Roll back global PyTorch to 2.0.1 and timm to 0.4.12.

### Stop Rules
- Do NOT install or upgrade any packages in the global environment beyond the rollback.
- Do NOT create the venvs — only write the plan. Actual venv creation belongs to the next runner session.

### Required Artifacts
- `README.md`, `lockfile_plan.md`, `tier_requirements.md`, `RESULT.md`, `DIFF_SUMMARY.md`

---

## EXP-0010: TorchXRayVision Label Contract & Preprocessing Test

### Hypothesis
TorchXRayVision's 18-label order, [-1024,1024] HU normalization, and output schema can be formalized as a CeXaR contract that catches mismatches early — and confirmed against CeXaR manifest expectations.

### Why It Matters
EXP-0002 showed XRV works but left 2 critical gaps: (a) license was not documented in RESULT.md, (b) label order was not cross-walked against CeXaR manifests. This experiment closes those gaps. It also provides data for whether XRV's `integration-candidate` status can be restored.

### Allowed Actions
- Read `manifests/01_baseline_manifest.md` and compare label expectations.
- Write a Python contract test script (`test_xrv_contract.py`) that:
  1. Confirms TorchXRayVision Apache 2.0 license by reading repo metadata.
  2. Loads DenseNet121 and verifies 18 pathology labels.
  3. Creates a label-mapping table between XRV labels and CeXaR manifest expected labels.
  4. Tests preprocessing contract: random tensor within [-1024, 1024] → normalized output.
  5. Tests output contract: forward pass output is always shape [B, 18].
- Run the script and log results.
- Write a `label_crosswalk.md` artifact.

### Stop Rules
- If TorchXRayVision import fails (e.g., due to PyTorch being rolled back), report the failure and recommend fixing the env first.
- If label order diverges from manifest expectations, document the gap — do not modify production code to fix it.
- Do NOT download datasets or run dataset wrappers.

### Required Artifacts
- `README.md`, `TEST_PLAN.md`, `RUNNER_INSTRUCTIONS.md`, `EXPERIMENT_LOG.md`, `RESULT.md`, `FAILURE_REPORT.md`, `DIFF_SUMMARY.md`, `configs/`, `artifacts/label_crosswalk.md`, `artifacts/test_xrv_contract.py`, `commands.ps1`

---

## EXP-0011: Quantus Metric Smoke Test (Minimal)

### Hypothesis
Quantus can produce at least one XAI evaluation metric (e.g., faithfulness correlation) on synthetic heatmaps and random model outputs, confirming it is functional before any integration consideration.

### Why It Matters
EXP-0005 awarded Quantus `integration-candidate` with zero runtime evidence. Before Quantus can be part of CeXaR's fidelity validation stack, its basic metric engine must be confirmed working.

### Allowed Actions
- Install quantus with full dependencies in a controlled manner.
- Create a synthetic test: random model output tensor, random heatmap tensor, and run at least 1 metric (e.g., `FaithfulnessCorrelation` or `MonotonicityCorrelation`).
- Record metric output, runtime, and edge cases.
- Document which metrics require ground-truth data (blocked) vs which work on synthetic data.

### Stop Rules
- If full dependency install triggers another PyTorch upgrade, stop and report the conflict.
- If no metric can produce a numeric result on synthetic data within 2 attempts, report as `blocked`.

### Required Artifacts
- `README.md`, `TEST_PLAN.md`, `RUNNER_INSTRUCTIONS.md`, `EXPERIMENT_LOG.md`, `RESULT.md`, `FAILURE_REPORT.md`, `DIFF_SUMMARY.md`, `configs/`, `artifacts/quantus_smoke_result.json`, `commands.ps1`