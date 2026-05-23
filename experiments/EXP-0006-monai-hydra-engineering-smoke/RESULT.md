# RESULT.md

## Verdict:
- **MONAI**: `engineering-candidate-requires-isolated-rerun`
- **Hydra**: `engineering-candidate-requires-isolated-rerun`

## Summary
MONAI 1.5.2 and Hydra 1.3.2 both installed and functioned during the original smoke test. However, the run is not integration-ready because it installed into the global Python environment and upgraded PyTorch from 2.0.1 to 2.12.0.

The technical smoke result is useful as a signal, but the experiment must be rerun in an isolated environment before any integration recommendation.

## Findings
- **MONAI version**: 1.5.2
- **MONAI set_determinism**: Works with seed control; minor floating-point variance in RandRotate due to interpolation (expected behavior)
- **MONAI transforms**: Compose works with medical imaging transforms (ScaleIntensity, RandRotate, etc.)
- **Hydra version**: 1.3.2
- **Hydra config**: Loads from YAML, supports hierarchical composition
- **PyTorch**: Upgraded from 2.0.1 to 2.12.0 (requirement for MONAI 1.5.2)

## Risks
- PyTorch upgrade (2.0.1 → 2.12.0) may affect other env components (e.g., torchvision image extension rebuild warning observed)
- Hydra config_dir requires absolute path
- MONAI's lazy transforms and MetaTensor may add overhead for simple pipelines

## Next Steps
- Rerun MONAI/Hydra in a dedicated isolated environment.
- Do not accept either as integration-ready from this run.
- Candidate seed policy to retest: `monai.set_determinism(seed)` + PyTorch deterministic flags.
- Candidate config policy to retest: Hydra YAMLs for dataset/model/eval configs.

## Audit Note

Audit Pass 2, 2026-05-23: Verdict downgraded from `integration-candidate` because the original run caused uncontrolled global environment mutation.
