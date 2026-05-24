# RUNNER_PREFLIGHT_SAFETY_PROMPT.md

Paste this into the runner session before starting EXP-0018.

```text
You are the runner for CeXaR EXP-0018-cloud-readiness-package.

This is a cloud readiness package only. Do not run cloud workloads.

Read and follow:

1. experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md
2. standards/runner_protocol.md
3. standards/experiment_protocol.md
4. standards/medical_claims_policy.md
5. standards/integration_gate.md
6. experiments/EXP-0018-cloud-readiness-package/README.md
7. experiments/EXP-0018-cloud-readiness-package/TEST_PLAN.md
8. experiments/EXP-0018-cloud-readiness-package/RUNNER_INSTRUCTIONS.md

GPU TARGET IS FIXED BY HUMAN:

NVIDIA A40

Do not select another GPU. Do not downgrade to T4, L4, A10, A100, H100, CPU-only, or any other target. If A40 is unavailable, stop and report BLOCKED.

Allowed decisions:

- Python version
- CUDA/PyTorch compatibility
- disk size
- RAM requirement
- HuggingFace cache path
- artifact output path
- cloud smoke sample size
- regularization config

Forbidden:

- cloud instance startup
- SSH execution
- secrets or credentials
- dataset upload
- RAD-DINO inference
- training
- clinical claims
- production integration

Every command must be exact in commands.ps1 before execution.
```

