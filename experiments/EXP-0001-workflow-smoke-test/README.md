# EXP-0001 Workflow Smoke Test

## Objective

Test whether the CeXaR controlled experiment workflow is understandable and executable without touching production code.

## Scope

This experiment does not clone repositories, install dependencies, train models, or evaluate medical performance.

## Expected Outcome

The runner should demonstrate that it can:

- Read relevant manifests and standards
- Follow the experiment boundary
- Log commands and observations
- Produce result, failure, and diff summary files
- Avoid unsupported medical claims

