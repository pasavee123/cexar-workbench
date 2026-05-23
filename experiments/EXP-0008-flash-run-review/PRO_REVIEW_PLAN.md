# CeXaR Pro Review Plan

This plan is for DeepSeek V4 Pro.

You are reviewing the previous Flash runner output. You are not repeating all experiments. Use Flash's outputs as evidence, verify the parts that affect decisions, and produce a clean review for Codex and the human owner.

## 1. Role

You are the reviewer and consolidator.

Your job is to:

- Audit whether Flash followed the plan.
- Identify missing required files or incomplete logs.
- Identify environment side effects.
- Downgrade overconfident claims.
- Decide which Flash findings are reliable enough to keep.
- Recommend the next 2-3 isolated experiments.

Do not act as an integration agent.

## 2. Must Read First

Read these files first, in order:

1. `standards/runner_protocol.md`
2. `standards/experiment_protocol.md`
3. `standards/medical_claims_policy.md`
4. `standards/integration_gate.md`
5. `standards/codex_review_protocol.md`
6. `experiments/DEEPSEEK_RUNNER_PLAN.md`
7. `experiments/RUNNER_SESSION_SUMMARY.md`

Then review these experiment folders:

1. `experiments/EXP-0002-torchxrayvision-inspect/`
2. `experiments/EXP-0003-rad-dino-inspect/`
3. `experiments/EXP-0004-biomedclip-chexzero-inspect/`
4. `experiments/EXP-0005-xai-trust-stack-inspect/`
5. `experiments/EXP-0006-monai-hydra-engineering-smoke/`
6. `experiments/EXP-0007-broad-candidate-triage/`

Read manifest files only when needed to audit a claim:

- `manifests/01_baseline_manifest.md`
- `manifests/02_split_protocol.md`
- `manifests/03_transformer_baselines.md`
- `manifests/04_explainability_methods.md`
- `manifests/05_fidelity_manifest.md`
- `manifests/06_heatmap_validation.md`
- `manifests/07_failure_modes.md`
- `manifests/08_research_roadmap.md`

## 3. Do Not

Do not:

- Install packages.
- Download model weights.
- Clone repositories.
- Run new model experiments.
- Modify production code.
- Modify `manifests/`.
- Modify `standards/`.
- Modify `repo_hunt/`.
- Rewrite Flash's existing experiment results.
- Delete files or caches.
- Make clinical claims.

If you need a command for audit, prefer read-only commands such as directory listing, file reading, and environment inspection.

## 4. Review Scope

For each Flash experiment, answer:

- Did it create all required files?
- Did it log commands and failures clearly?
- Did it stay inside the allowed write scope?
- Did it install packages, upgrade packages, download weights, or create caches?
- Are verdict labels supported by evidence?
- Should any `integration-candidate` verdict be downgraded?
- What evidence is strong enough to preserve?
- What evidence requires a follow-up experiment?

## 5. Claim Downgrade Policy

Use conservative labels.

If Flash wrote `integration-candidate`, downgrade unless there is strong evidence for all of:

- License checked
- Version and dependencies documented
- Minimal smoke test passed
- Preprocessing assumptions documented
- Output shape/interface documented
- No uncontrolled environment side effect
- Next integration boundary is clear

Prefer these labels:

- `reliable-inspect-result`
- `promising-benchmark-candidate`
- `needs-controlled-rerun`
- `reference-only`
- `blocked`
- `do-not-integrate-yet`

Remember: no production integration is approved by this review.

## 6. Environment Side Effect Audit

Create a report of:

- Packages Flash installed
- Packages Flash upgraded
- PyTorch / torchvision / transformers / MONAI / Hydra / open_clip versions, if inspectable
- Model weights or caches created
- Any changes outside `experiments/`
- Any risk caused by package upgrades

If Python is unavailable in the current shell, say so clearly and use file logs as evidence instead.

## 7. Required Output Files

Write only inside:

`experiments/EXP-0008-flash-run-review/`

Create these files:

- `PRO_REVIEW_RESULT.md`
- `ENVIRONMENT_SIDE_EFFECTS.md`
- `CLAIMS_AUDIT.md`
- `NEXT_EXPERIMENTS.md`
- `DIFF_SUMMARY.md`

## 8. Output Requirements

### PRO_REVIEW_RESULT.md

Include:

- Overall verdict on Flash's run
- Which findings are reliable
- Which findings are weak
- Which findings should be rerun
- Whether Flash followed the plan

### ENVIRONMENT_SIDE_EFFECTS.md

Include:

- Installed/upgraded packages
- Weights/cache paths
- Environment risks
- Recommended cleanup or isolation plan

### CLAIMS_AUDIT.md

Include a table:

| Flash Claim | Evidence | Pro Verdict | Action |
|---|---|---|---|

### NEXT_EXPERIMENTS.md

Recommend only 2-3 next experiments.

Each recommendation must include:

- Experiment name
- Hypothesis
- Why it matters
- Allowed actions
- Stop rules
- Required artifacts

### DIFF_SUMMARY.md

List only the files Pro created or changed.

## 9. Recommended Next Experiment Bias

Prefer next experiments that increase reliability without broad uncontrolled installation.

Good next experiments:

- Environment isolation and lockfile plan
- TorchXRayVision label/preprocessing contract test
- BiomedCLIP prompt/output contract test
- XAI heatmap schema and metric schema test
- RAD-DINO weight-download approval plan

Avoid:

- Full training
- Large dataset downloads
- Production integration
- New broad repo-hunt sprawl

