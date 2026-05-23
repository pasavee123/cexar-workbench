# CeXaR Codex Review Protocol

Codex reviews experiment outputs before any integration decision.

## Required Review Inputs

Codex must read:

- `TEST_PLAN.md`
- `RUNNER_INSTRUCTIONS.md`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- Artifacts relevant to the test
- Referenced manifests
- Referenced repo-hunt candidate review

## Review Questions

Codex must decide:

- Did the runner follow the plan?
- Were commands and failures logged honestly?
- Were experiment boundaries respected?
- Did the test evaluate the stated hypothesis?
- Are metrics complete enough for the claim?
- Are patient leakage, label mapping, preprocessing, and threshold risks addressed?
- Are XAI or heatmap outputs validated numerically rather than visually only?
- Should the candidate be rejected, retried, modified, or proposed for integration?

## Review Output

Codex writes `REVIEW.md` with:

- Verdict: pass, fail, retry, reject, or needs-human-decision
- Evidence summary
- Risk summary
- Missing evidence
- Recommended next action
- Whether production integration is allowed

Production integration is never allowed without explicit human approval.

