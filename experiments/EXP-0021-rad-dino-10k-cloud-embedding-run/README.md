# EXP-0021 RAD-DINO 10k Cloud Embedding Run

## Purpose

Run a controlled 10,000-image RAD-DINO embedding extraction on CheXpert using the validated RunPod RTX 6000 Ada environment from EXP-0020.

This experiment is a scale-up embedding production rehearsal. It must not perform model training, classifier fitting, AUROC/AUPRC calculation, clinical evaluation, clinical claims, or production integration.

## Strategy

EXP-0021 is split into two controlled phases:

- Phase A: DeepSeek authors or updates the one-shot scripts and performs small dry-run checks only.
- Phase B: Codex reviews the scripts and then controls the cloud execution/documentation gate before the 10k run.

DeepSeek may write implementation code, but it must stop before the real 10k run until Codex reviews the scripts.

## Required Runtime

- GPU: NVIDIA RTX 6000 Ada Generation
- Image: `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858`
- Repository checkout: `/root/cexar-workbench`
- Persistent network volume: `/workspace`
- Dataset root: `/workspace/chexpert_dataset_raw`
- Hugging Face cache: `/workspace/.cache/huggingface`
- Torch cache: `/workspace/.cache/torch`
- Large output artifact root: `/workspace/exp_artifacts/EXP-0021`

## Core Path Mapping

The EXP-0016 Windows manifest paths include `archive/`, while the RunPod dataset root does not. Use this mapping:

```text
D:\Dataset_Chexpert\archive -> /workspace/chexpert_dataset_raw
```

## Expected Outputs

Large outputs must stay outside git:

```text
/workspace/exp_artifacts/EXP-0021/
  runs/
    dryrun5/
    dryrun100/
    full_10k/
      manifests/candidate_manifest_10k.csv
      embeddings/shard_0000.npz
      embeddings/...
      checkpoints/progress.json
      summaries/exp0021_summary.json
```

Git-tracked outputs should be lightweight summaries and documentation only.
