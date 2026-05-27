# RUNNER_PREFLIGHT_SAFETY_PROMPT.md

You are the runner for CeXaR EXP-0022-rad-dino-throughput-optimization.

Before doing anything, read:

- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/RESULT.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/README.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/TEST_PLAN.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/RUNNER_INSTRUCTIONS.md`
- `experiments/EXP-0022-rad-dino-throughput-optimization/configs/exp0022_config.yaml`

Critical runtime facts:

- Repository checkout path: `/root/cexar-workbench`
- Persistent network volume: `/workspace`
- Required GPU: NVIDIA RTX 6000 Ada Generation
- Required Python: `/opt/venv/bin/python`
- Large artifact root: `/workspace/exp_artifacts/EXP-0022`
- Do not push from the Pod unless the human explicitly asks.

Your job:

1. Implement the EXP-0022 scripts.
2. Run the benchmark.
3. Generate a review packet tarball.
4. Stop and report the packet path.

Do not train, classify, compute clinical metrics, make clinical claims, delete datasets, or modify production code.

