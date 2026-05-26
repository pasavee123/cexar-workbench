# DATA_ASSET_MANIFEST.md

## Purpose

Document the external data assets available on the RunPod Network Volume for EXP-0020.

No dataset files are committed to Git.

## Network Volume Snapshot

Recorded by the human on 2026-05-26:

```text
/workspace mounted from mfs#us-wa-1.runpod.net:9421
Filesystem size: 479T
Used: 287T
Available: 192T
Use%: 60%
```

## Dataset Assets

| Asset | Path | Size | Purpose |
|-------|------|------|---------|
| CheXpert raw dataset | `/workspace/chexpert_dataset_raw` | included in 66G combined dataset usage | Primary EXP-0020 RAD-DINO smoke input |
| NIH14 raw dataset | `/workspace/nih_dataset_raw` | included in 66G combined dataset usage | Future external dataset experiments, not used in EXP-0020 |

Human correction on 2026-05-26:

```text
Actual combined Network Volume usage for both datasets is approximately 66G.
```

Earlier larger per-folder numbers should not be treated as authoritative until re-measured by the runner inside the pod.

## NIH14 Observed Structure

```text
/workspace/nih_dataset_raw
/workspace/nih_dataset_raw/ARXIV_V5_CHESTXRAY.pdf
/workspace/nih_dataset_raw/BBox_List_2017.csv
/workspace/nih_dataset_raw/Data_Entry_2017.csv
/workspace/nih_dataset_raw/FAQ_CHESTXRAY.pdf
/workspace/nih_dataset_raw/LOG_CHESTXRAY.pdf
/workspace/nih_dataset_raw/README_CHESTXRAY.pdf
/workspace/nih_dataset_raw/images_001
/workspace/nih_dataset_raw/images_002
/workspace/nih_dataset_raw/images_003
/workspace/nih_dataset_raw/images_004
/workspace/nih_dataset_raw/images_005
```

## CheXpert Path Contract

The EXP-0016 manifest contains local Windows paths rooted at:

```text
D:\Dataset_Chexpert
```

EXP-0020 maps that prefix to:

```text
/workspace/chexpert_dataset_raw
```

Therefore a manifest path such as:

```text
D:\Dataset_Chexpert\archive\train\...
```

should resolve to:

```text
/workspace/chexpert_dataset_raw/archive/train/...
```

## Optional Compatibility Symlink

If needed, the runner may create:

```bash
mkdir -p /mnt
ln -sfn /workspace/chexpert_dataset_raw /mnt/chexpert
```

The exact command must be registered in `commands.ps1` before execution.

## Deletion Policy

Do not delete dataset roots during EXP-0020.

Allowed cleanup:
- temporary local run files inside this experiment folder
- failed partial artifacts created by EXP-0020 after exact command registration

Forbidden cleanup:
- `/workspace/chexpert_dataset_raw`
- `/workspace/nih_dataset_raw`
- `/workspace/.cache/huggingface` unless explicitly approved by the human
