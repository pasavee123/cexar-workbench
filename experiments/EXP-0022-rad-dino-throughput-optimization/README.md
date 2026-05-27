# EXP-0022 RAD-DINO Throughput Optimization

## Purpose

Benchmark and optimize the RAD-DINO CheXpert embedding pipeline before any full-dataset extraction.

EXP-0021 proved that 10,000 images can be embedded successfully, but the observed utilization pattern suggested a CPU/image-preprocessing bottleneck. EXP-0022 must identify a better batch/DataLoader configuration before spending more cloud time on larger runs.

## Scope

This is a performance engineering experiment only.

Allowed:

- Benchmark RAD-DINO embedding throughput on a bounded sample.
- Compare batch sizes and DataLoader worker counts.
- Measure runtime, images/sec, CPU/GPU memory, and coarse GPU utilization.
- Produce a recommended config for future full-dataset extraction.

Forbidden:

- No model training.
- No classifier/probe fitting.
- No AUROC/AUPRC or clinical metric calculation.
- No clinical claims.
- No production integration.
- No dataset deletion or cache cleanup.
- No GitHub auth required on the Pod.

## Required Runtime

- GPU: NVIDIA RTX 6000 Ada Generation
- Image: `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858`
- Repository checkout: `/root/cexar-workbench`
- Persistent network volume: `/workspace`
- Dataset root: `/workspace/chexpert_dataset_raw`
- Existing EXP-0021 manifest/artifacts may be used as input.

## Output Strategy

The Pod should produce a self-contained review packet:

```text
/workspace/exp_artifacts/EXP-0022/review_packet/exp0022_review_packet.tar.gz
```

The human can download this one small package to local and shut down the Pod. Codex local then reviews, finalizes docs, and pushes GitHub.

