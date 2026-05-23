# CeXaR DeepSeek Runner Plan

This file is the starting plan for a runner model such as DeepSeek.

You are the runner, not the architect. Your job is to run many useful isolated experiments, inspect candidates deeply, log everything, and report back clearly so Codex and the human owner can decide what to integrate later.

Do not modify production code. Do not integrate external repositories into the real system. Work inside `experiments/` unless a plan explicitly allows read-only inspection elsewhere.

## 1. Session Start Reading Order

At the start of every session, read these files first:

1. `standards/runner_protocol.md`
2. `standards/experiment_protocol.md`
3. `standards/medical_claims_policy.md`
4. `standards/integration_gate.md`
5. `manifests/README.md`
6. `repo_hunt/candidates/deep-research-report.md`
7. This file: `experiments/DEEPSEEK_RUNNER_PLAN.md`

Then read any manifest related to the experiment you are about to run:

- Baseline/model experiments: `manifests/01_baseline_manifest.md`
- Split/evaluation experiments: `manifests/02_split_protocol.md`
- Transformer/foundation model experiments: `manifests/03_transformer_baselines.md`
- Explainability experiments: `manifests/04_explainability_methods.md`
- Fidelity experiments: `manifests/05_fidelity_manifest.md`
- Heatmap/localization experiments: `manifests/06_heatmap_validation.md`
- Failure/shortcut/bias experiments: `manifests/07_failure_modes.md`
- Roadmap experiments: `manifests/08_research_roadmap.md`

## 2. Core Behavior

Be curious and practical. Test enough to be useful, but keep every test isolated, reproducible, and reviewable.

You may explore multiple candidate approaches inside `experiments/`, but every experiment must have:

- `README.md`
- `TEST_PLAN.md`
- `RUNNER_INSTRUCTIONS.md`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`
- `configs/`
- `artifacts/`
- `commands.ps1`

If you create extra scripts, configs, notes, or artifacts, keep them inside the experiment folder.

## 3. Global Safety Rules

Do not:

- Modify production code
- Modify `manifests/`
- Modify `standards/`
- Modify `repo_hunt/` source files
- Claim clinical usefulness, diagnostic readiness, or radiologist-level performance
- Tune thresholds on test data
- Hide failed commands
- Delete failed artifacts to make results look cleaner
- Use external repositories as trusted just because they are popular

You may:

- Read manifests, standards, and repo-hunt files
- Create new experiment folders
- Write logs, results, configs, and artifacts inside experiment folders
- Inspect docs and local files
- Propose future production patches in reports
- Try multiple implementation paths inside the experiment scope

## 4. Attempt Budget

Use this attempt policy unless a specific experiment overrides it.

Per candidate:

- Maximum 3 major attempts.
- Maximum 2 retries for the same repeated command/setup failure.
- Maximum 60 minutes of active work per experiment before writing a status result or failure report.

Stop immediately and report when:

- Gated access, credentials, private data, or manual approval is required
- A dependency conflict repeats twice
- You need to modify files outside the experiment folder
- Patient split, label order, preprocessing, or metric assumptions are unclear
- A command would download large data or large model weights without approval
- A command would require production integration

If blocked, write `FAILURE_REPORT.md`. Do not guess endlessly.

## 5. Logging Standard

Every command must be logged in `EXPERIMENT_LOG.md` with:

- Timestamp
- Working directory
- Command
- Exit code
- Short stdout summary
- Short stderr/error summary
- Files created or changed
- Interpretation of the result

Every experiment must end with:

- `RESULT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`

If any step fails, update `FAILURE_REPORT.md`.

## 6. Experiment Queue

Run these experiments in order unless the human owner or Codex gives a newer instruction.

### EXP-0002 TorchXRayVision Inspect

Folder:

`experiments/EXP-0002-torchxrayvision-inspect/`

Goal:

Decide whether TorchXRayVision should become CeXaR's baseline/data benchmark layer.

Try:

- Inspect repository docs, license, installation path, model API, dataset wrappers, preprocessing assumptions, and label order.
- Identify whether synthetic tensor smoke tests are possible without downloading datasets.
- If installation is allowed and lightweight, try import/load-model smoke test.
- Check whether output labels align with CeXaR manifest expectations.
- Check risks around normalization mismatch and dataset harmonization.

Stop if:

- Dependency install conflicts twice.
- It requires large downloads.
- Label mapping or preprocessing cannot be identified.

Report:

- `reject`, `reference-only`, `retry`, `benchmark-candidate`, or `integration-candidate`.

### EXP-0003 RAD-DINO Inspect

Folder:

`experiments/EXP-0003-rad-dino-inspect/`

Goal:

Decide whether RAD-DINO should be tested as a frozen foundation backbone for CeXaR.

Try:

- Inspect model card, license/terms, preprocessing, expected image size, embedding shape, and model loading API.
- Identify whether a synthetic tensor or tiny local image smoke test is possible.
- Compare assumptions against `manifests/03_transformer_baselines.md`.
- Record what is public, gated, private, or not reproducible.

Stop if:

- Access requires credentials or gated approval.
- Model weights are too large for the current session.
- Preprocessing or output shape cannot be established.

### EXP-0004 BiomedCLIP And CheXzero Inspect

Folder:

`experiments/EXP-0004-biomedclip-chexzero-inspect/`

Goal:

Compare BiomedCLIP and CheXzero as zero-shot or representation baselines.

Try:

- Inspect model/repo availability.
- Compare prompt format, preprocessing, checkpoint availability, license, and expected output.
- Identify whether either candidate can run a smoke test without datasets.
- Record which one is better suited as a benchmark, not as production infra.

Stop if:

- Checkpoints are inaccessible.
- Prompt/evaluation assumptions are too unclear.
- Setup requires large downloads without approval.

### EXP-0005 XAI Trust Stack Inspect

Folder:

`experiments/EXP-0005-xai-trust-stack-inspect/`

Goal:

Determine whether `pytorch-grad-cam`, `Captum`, `Quantus`, and `CheXlocalize` can form CeXaR's explainability and fidelity validation stack.

Try:

- Inspect API compatibility with CNN and ViT models.
- Identify minimal heatmap generation path.
- Identify minimal heatmap evaluation path.
- Map each tool to CeXaR outputs: raw heatmap, overlay, metadata, IoU, pointing game, sanity checks.
- Check license and maintenance risk.

Stop if:

- A tool requires unavailable data or model weights.
- Quantitative evaluation cannot be defined.
- A method only produces visually pleasing heatmaps without fidelity checks.

### EXP-0006 MONAI Hydra Engineering Smoke

Folder:

`experiments/EXP-0006-monai-hydra-engineering-smoke/`

Goal:

Decide whether MONAI + Hydra should become the first engineering layer for data transforms, determinism, and experiment config.

Try:

- Inspect MONAI deterministic controls and transform patterns.
- Inspect Hydra config composition patterns.
- Create a dummy config and tiny deterministic transform smoke test if lightweight.
- Record seed policy, config override policy, and run metadata fields CeXaR should require.

Stop if:

- Setup becomes larger than a smoke test.
- Dependency conflict repeats twice.

### EXP-0007 Broad Candidate Triage

Folder:

`experiments/EXP-0007-broad-candidate-triage/`

Goal:

Use remaining time to inspect more candidates from `deep-research-report.md` and sort them into useful buckets.

Candidates to consider:

- OpenCXR
- EVA-X
- BioViL-T
- CheXFound
- CXR-CLIP
- MedCLIP
- MS-CXR
- Transformer-Explainability
- vit-explain
- saliency sanity-check repositories
- MLflow
- W&B
- Lightning
- timm
- open_clip

For each candidate, record:

- Purpose
- URL
- License risk
- Maintenance signal
- Dependency risk
- CeXaR compatibility
- Recommended status
- Next experiment, if any

Do not install or run everything. Triage broadly, then recommend the best next isolated experiments.

## 7. Creativity Budget

You are allowed to propose extra experiments if you find a promising angle, as long as:

- The experiment stays isolated.
- It has a clear hypothesis.
- It logs all commands and outcomes.
- It does not modify production code.
- It does not make unsupported medical claims.

Good extra experiment ideas:

- Synthetic tensor smoke tests for model input/output contracts.
- Label-order audit scripts using fake labels.
- Preprocessing mismatch demonstrations using toy tensors.
- Heatmap shape and metadata schema tests.
- Config reproducibility tests.
- Candidate license/maintenance comparison tables.
- Failure-mode checklists mapped to each candidate.

Bad extra experiment ideas:

- Full training without a reviewed test plan.
- Downloading large medical datasets without approval.
- Integrating a repo directly into production.
- Reporting clinical performance from toy data.

## 8. Final Report Format

At the end of your session, create or update:

`experiments/RUNNER_SESSION_SUMMARY.md`

Use this format:

```md
# Runner Session Summary

## Session Scope

[What was attempted.]

## Experiments Created Or Updated

| Experiment | Status | Main Result | Next Action |
|---|---|---|---|

## Best Candidates

| Candidate | Recommended Status | Why |
|---|---|---|

## Rejected Or Risky Candidates

| Candidate | Reason |
|---|---|

## Blockers

- [Blocker]

## Files Changed

- [File]

## What Codex Should Review First

1. [Experiment/result]
2. [Experiment/result]
3. [Experiment/result]
```

## 9. Status Labels

Use these labels consistently:

- `reject`
- `reference-only`
- `inspect-more`
- `retry`
- `benchmark-candidate`
- `integration-candidate`
- `blocked`

Remember: `integration-candidate` does not mean integration is approved. Codex review and human approval are still required.

