# CODEX_LOCAL_REVIEW_PLAN.md

## Goal

Codex local should review the EXP-0022 review packet after the human downloads it from the Pod.

## Review Inputs

Expected local packet contents:

- `benchmark_results.csv`
- `benchmark_results.json`
- `recommended_config.json`
- `RESULT_DRAFT.md`
- `FAILURE_REPORT_DRAFT.md`
- `EXPERIMENT_LOG_AUTO.md`
- `DIFF_SUMMARY_AUTO.md`
- `artifact_manifest.json`

## Review Tasks

- Verify benchmark table consistency.
- Verify recommended config is supported by evidence.
- Verify no clinical claims or clinical metrics are present.
- Verify no large `.npz` artifacts were packaged.
- Update EXP-0022 docs in git.
- Commit/push from local only.

## Possible Verdicts

- `APPROVE_THROUGHPUT_CONFIG`
- `REQUEST_BENCHMARK_RERUN`
- `REJECT_AND_REPLAN`

