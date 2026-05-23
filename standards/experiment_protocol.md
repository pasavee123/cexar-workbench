# CeXaR Experiment Protocol

This protocol defines how CeXaR experiments are planned, executed, logged, reviewed, and either rejected or promoted for human approval.

## Core Rule

No production integration is allowed until an isolated experiment has passed Codex review and human approval.

## Required Inputs

Every experiment must identify:

- Relevant manifests from `manifests/`
- Candidate source, if any, from `repo_hunt/candidates/`
- Hypothesis being tested
- Expected outputs
- Pass/fail criteria
- Known medical, ML, and engineering risks

## Required Files

Each experiment folder must contain:

- `README.md`
- `TEST_PLAN.md`
- `RUNNER_INSTRUCTIONS.md`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW.md`
- `configs/`
- `artifacts/`
- `commands.ps1`

## Experiment Boundaries

Runner agents must work inside the experiment folder unless the test plan explicitly allows reading another path.

Runner agents must not:

- Modify production code
- Install dependencies without approval
- Download external repositories without approval
- Change manifests or standards
- Claim clinical performance beyond measured evidence

## Success Criteria

An experiment passes only when:

- The required commands are logged
- The output artifacts are present or the missing artifacts are explained
- The pass/fail criteria are evaluated
- The risks are documented
- The result is reviewable by Codex and a human

## Failure Criteria

An experiment fails when:

- Patient-level leakage cannot be ruled out
- Label order or preprocessing assumptions are unclear
- Metrics are incomplete or not reproducible
- Runner modifies files outside its allowed scope
- Medical claims exceed the evidence
- Repeated failures occur without a clear recovery path

