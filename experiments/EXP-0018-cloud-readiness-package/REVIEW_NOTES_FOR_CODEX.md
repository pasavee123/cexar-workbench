# REVIEW_NOTES_FOR_CODEX.md

## Review Checklist

Codex should verify:

- NVIDIA A40 is fixed as the GPU target.
- No alternative GPU was selected by the runner.
- No secrets, hostnames, tokens, or SSH keys were committed.
- No cloud commands were executed.
- No dataset upload occurred.
- No RAD-DINO inference or model training occurred.
- Configs are machine-readable.
- Code files are skeletons only.
- EXP0019 readiness is explicit.

