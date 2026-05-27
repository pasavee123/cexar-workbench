# REVIEW_NOTES_FOR_CODEX.md

EXP-0022 should be reviewed locally from a downloaded review packet. AI should not be required on the Pod for normal execution.

Codex pre-run note: benchmark timing must measure end-to-end batch throughput, including DataLoader fetch and GPU inference after warmup. A GPU-only forward timing would miss the CPU/I/O bottleneck that EXP-0022 is designed to diagnose.
