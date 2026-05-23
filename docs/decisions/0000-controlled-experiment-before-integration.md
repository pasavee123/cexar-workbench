# 0000-controlled-experiment-before-integration

* Status: proposed
* Deciders: CeXaR human owner, Codex
* Date: 2026-05-22

## Context And Problem Statement

CeXaR is a medical AI project for chest X-ray analysis. New models, visualization methods, external repositories, datasets, and tools can introduce patient safety risk, data leakage, reproducibility gaps, license issues, and unsupported medical claims.

## Decision Drivers

- Medical AI work must be reviewable and reproducible.
- External repositories are not trusted by default.
- Runner agents need strict boundaries.
- Production code must not be modified before experiment review and human approval.

## Considered Options

- Integrate promising components directly.
- Test components in isolated experiments first.
- Keep all external sources as background research only.

## Decision Outcome

Chosen option: test components in isolated experiments first, because it provides a controlled path from research intake to runner execution, Codex review, and human approval.

## Consequences

- Good: Safer integration workflow, clearer audit trail, easier rollback.
- Bad: More documentation overhead before implementation.

