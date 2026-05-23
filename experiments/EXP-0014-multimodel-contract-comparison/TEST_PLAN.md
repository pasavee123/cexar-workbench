# TEST_PLAN.md

## Goal

Create a clean comparison between XRV DenseNet121 pathology-score outputs and RAD-DINO embedding outputs using the same image sample.

The result should clarify how CeXaR can support multiple model families without mixing classifier outputs, embeddings, labels, and metrics incorrectly.

## Non-Goals

- Do not run new inference if existing artifacts are readable.
- Do not train.
- Do not classify RAD-DINO embeddings.
- Do not compute AUROC or any new clinical metric.
- Do not tune thresholds.
- Do not decide production integration.

## Required Inputs

From EXP-0012B:

- `artifacts/sample_manifest.csv`
- `artifacts/xrv_chexpert_outputs.csv`
- `artifacts/metric_sanity.json`

From EXP-0013:

- `artifacts/rad_dino_embedding_summary.json`
- `artifacts/rad_dino_embeddings.npz`

## Phase 0: Safety And Ledger

1. Read `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`.
2. Read `standards/runner_protocol.md`.
3. Read `standards/experiment_protocol.md`.
4. Read `standards/medical_claims_policy.md`.
5. Read `standards/integration_gate.md`.
6. Create/update `commands.ps1` before any command.
7. Register every command in `commands.ps1` before execution.

Strict constraints:

- Do not modify global Python.
- Do not install packages.
- Do not delete, move, or clean up artifacts unless explicitly instructed and approved.
- Do not modify EXP-0012B or EXP-0013 artifacts.
- Do not modify production code, manifests, standards, or repo_hunt.

## Phase 1: Artifact Availability Check

Verify all required input artifacts exist.

If any required artifact is missing:

- Stop.
- Write `FAILURE_REPORT.md`.
- Do not regenerate the missing artifact unless Codex/human explicitly approves a rerun.

## Phase 2: Sample Alignment Check

Confirm whether XRV and RAD-DINO outputs refer to the same 100-image sample.

Check:

- `sample_manifest.csv` has 100 rows.
- `xrv_chexpert_outputs.csv` has 100 rows.
- `rad_dino_embedding_summary.json` reports 100 attempted and 100 succeeded.
- `rad_dino_embeddings.npz` has shape `[100, 768]`.
- RAD-DINO embedding indices, if present, align with sample manifest indices.

Output:

```text
artifacts/sample_alignment_report.json
```

The report must include:

- sample count
- XRV output count
- RAD-DINO output count
- RAD-DINO embedding shape
- alignment status
- any mismatch details

## Phase 3: Output Contract Comparison

Compare model families:

### XRV DenseNet121

- model family: supervised chest X-ray classifier
- output type: pathology scores/logits
- output shape: `[N, 18]`
- label space: explicit 18 XRV pathologies
- direct CheXpert mapping: partial, from EXP-0012B
- can compute label metrics: yes, only for mapped labels and valid evaluation design

### RAD-DINO

- model family: foundation image encoder / embedding backbone
- output type: image embeddings
- output shape: `[N, 768]`
- label space: none
- direct CheXpert mapping: none
- can compute label metrics directly: no
- requires downstream head/probe for classification

Output:

```text
artifacts/model_output_contract_comparison.json
```

## Phase 4: CeXaR Adapter Contract Draft

Draft a generic CeXaR model adapter contract that can represent both classifier models and embedding backbones.

Output:

```text
artifacts/cexar_adapter_contract_draft.md
```

The draft must include fields such as:

- `model_id`
- `model_family`
- `input_manifest`
- `num_images`
- `preprocessing_contract`
- `output_type`
- `output_shape`
- `label_space`
- `embedding_dim`
- `requires_downstream_head`
- `can_compute_direct_metrics`
- `clinical_claims_allowed`
- `artifact_paths`
- `known_limitations`

## Phase 5: Final Result

`RESULT.md` must clearly state one of:

- PASS AS MULTI-MODEL CONTRACT COMPARISON
- PARTIAL PASS
- FAILED / BLOCKED

## Pass Criteria

Pass if:

- Required artifacts are readable.
- Sample alignment is verified or any mismatch is clearly documented.
- XRV and RAD-DINO output contracts are correctly distinguished.
- Adapter contract draft is written.
- No new inference, training, AUROC, classification, or production integration occurs.

## Stop Conditions

Stop and write `FAILURE_REPORT.md` if:

- Required artifacts are missing.
- Artifact shape cannot be verified.
- The runner would need to install packages.
- The runner would need to modify or regenerate prior experiment artifacts.
- The runner believes the contract comparison is logically unsafe and needs architecture review.

## Required Artifacts

- `README.md`
- `TEST_PLAN.md`
- `RUNNER_INSTRUCTIONS.md`
- `RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`
- `commands.ps1`
- `artifacts/sample_alignment_report.json`
- `artifacts/model_output_contract_comparison.json`
- `artifacts/cexar_adapter_contract_draft.md`
- `artifacts/run_contract_comparison.py`
- `configs/`
