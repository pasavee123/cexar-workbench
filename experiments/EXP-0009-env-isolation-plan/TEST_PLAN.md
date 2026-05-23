# TEST_PLAN.md

## Plan

1. Analyze environment contamination documented by EXP-0008.
2. Design isolated venv tiers for baseline, foundation, XAI, and training experiments.
3. Write pinned requirements files for each tier.
4. Write the next-run prompt for TorchXRayVision baseline inference.

## Success Criteria

- No packages are installed.
- No global rollback is performed.
- Isolated environment requirements are documented.
- Future runners are instructed to avoid global Python.

## Audit Note

Audit Pass 2, 2026-05-23: This file was created retroactively to close required-file gaps.
