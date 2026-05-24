# POST_AUDIT_CLEANUP.md

## Status

Post-audit cleanup planned after evidence snapshot.

## Evidence Snapshot

Wrong-path artifacts from EXP-0015 were intentionally committed as audit evidence in:

```text
097c457 chore: record EXP-0015 linear probe smoke test
```

That commit preserves the original evidence for review.

## Cleanup Scope

After the evidence snapshot, the following wrong-path artifact copies may be removed from the active repository tree:

```text
D:\cexar-workbench\experiments\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json
D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json
```

The canonical artifact remains:

```text
D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json
```

## Rationale

This cleanup keeps the active repository tree readable while preserving the audit trail in Git history.

