#!/usr/bin/env python3
"""EXP-0021: Build deterministic 10,000-image manifest from CheXpert dataset.

Reads train.csv and valid.csv from the dataset root, resolves image paths,
prefers frontal images, and selects a deterministic sample.

RunPod paths:
  Dataset: /workspace/chexpert_dataset_raw
  Output:  /workspace/exp_artifacts/EXP-0021/manifests/candidate_manifest_10k.csv
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

CHEXPERT_LABELS = [
    "Atelectasis",
    "Consolidation",
    "Pneumothorax",
    "Edema",
    "Pleural Effusion",
    "Pneumonia",
    "Cardiomegaly",
    "Lung Lesion",
    "Fracture",
    "Lung Opacity",
    "Enlarged Cardiomediastinum",
]


def resolve_path(csv_path, dataset_root):
    csv_path = csv_path.replace("\\", "/")
    dataset_root = dataset_root.rstrip("/")
    prefix = "CheXpert-v1.0-small/"
    if csv_path.startswith(prefix):
        return dataset_root + "/" + csv_path[len(prefix):]
    return os.path.join(dataset_root, csv_path)


def extract_patient_id(csv_path):
    parts = csv_path.replace("\\", "/").split("/")
    for p in parts:
        if p.startswith("patient"):
            return p
    return "UNKNOWN"


def main():
    parser = argparse.ArgumentParser(description="EXP-0021 manifest builder")
    parser.add_argument(
        "--dataset-root",
        default="/workspace/chexpert_dataset_raw",
    )
    parser.add_argument(
        "--output-csv",
        default="/workspace/exp_artifacts/EXP-0021/manifests/candidate_manifest_10k.csv",
    )
    parser.add_argument(
        "--num-images",
        type=int,
        default=10000,
        help="Target number of images to select",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260527,
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Override --num-images for dry-run (also limits CSV reading)",
    )
    args = parser.parse_args()

    dataset_root = os.path.abspath(args.dataset_root)
    train_csv = os.path.join(dataset_root, "train.csv")
    valid_csv = os.path.join(dataset_root, "valid.csv")

    if not os.path.isfile(train_csv):
        print(f"ERROR: train.csv not found at {train_csv}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(valid_csv):
        print(f"ERROR: valid.csv not found at {valid_csv}", file=sys.stderr)
        sys.exit(1)

    target_images = args.limit if args.limit is not None else args.num_images
    is_dry_run = args.limit is not None

    print(f"Reading {train_csv} ...")
    train_df = pd.read_csv(train_csv)
    print(f"Reading {valid_csv} ...")
    valid_df = pd.read_csv(valid_csv)

    if is_dry_run:
        read_limit = max(target_images * 2, 20)
        train_df = train_df.head(read_limit)
        valid_df = valid_df.head(read_limit)
        print(f"DRY-RUN: limited to {read_limit} rows from each CSV")
        print(f"DRY-RUN: target output = {target_images} images")

    print(f"Train rows (loaded): {len(train_df)}")
    print(f"Valid rows (loaded): {len(valid_df)}")

    train_df["resolved_path"] = train_df["Path"].apply(lambda p: resolve_path(p, dataset_root))
    valid_df["resolved_path"] = valid_df["Path"].apply(lambda p: resolve_path(p, dataset_root))

    train_df["patient_id"] = train_df["Path"].apply(extract_patient_id)
    valid_df["patient_id"] = valid_df["Path"].apply(extract_patient_id)

    train_df["source_csv"] = "train"
    valid_df["source_csv"] = "valid"
    train_df["csv_row_idx"] = train_df.index
    valid_df["csv_row_idx"] = valid_df.index

    combined = pd.concat([train_df, valid_df], ignore_index=True)

    path_exists = combined["resolved_path"].apply(os.path.exists)
    combined_valid = combined[path_exists].copy()
    print(f"Images with resolved existing paths: {len(combined_valid)} / {len(combined)}")

    if len(combined_valid) < target_images:
        print(
            f"ERROR: Only {len(combined_valid)} existing images found; need {target_images}",
            file=sys.stderr,
        )
        sys.exit(1)

    frontal_mask = combined_valid["Frontal/Lateral"] == "Frontal"
    frontal_df = combined_valid[frontal_mask].copy()
    non_frontal_df = combined_valid[~frontal_mask].copy()

    print(f"Frontal images available: {len(frontal_df)}")
    print(f"Non-frontal images available: {len(non_frontal_df)}")

    rng = np.random.RandomState(args.seed)

    target = min(target_images, len(combined_valid))
    if len(frontal_df) >= target:
        selected = frontal_df.sample(n=target, random_state=rng)
    else:
        selected_frontal = frontal_df.copy()
        remaining = target - len(selected_frontal)
        if remaining > 0 and len(non_frontal_df) > 0:
            selected_non_frontal = non_frontal_df.sample(
                n=min(remaining, len(non_frontal_df)), random_state=rng
            )
            selected = pd.concat([selected_frontal, selected_non_frontal], ignore_index=True)
        else:
            selected = selected_frontal.copy()

    selected = selected.sample(frac=1, random_state=rng).reset_index(drop=True)

    label_cols = [c for c in CHEXPERT_LABELS if c in selected.columns]
    if len(label_cols) < len(CHEXPERT_LABELS):
        missing = sorted(set(CHEXPERT_LABELS) - set(label_cols))
        print(f"WARNING: {len(missing)} expected label columns missing from CSVs: {missing}")

    keep_cols = ["resolved_path", "patient_id", "source_csv", "csv_row_idx",
                  "Frontal/Lateral", "Sex", "Age", "AP/PA"] + label_cols

    metadata_cols = ["Sex", "Frontal/Lateral", "AP/PA"]
    for col in metadata_cols:
        if col not in selected.columns:
            selected[col] = ""

    manifest = selected[keep_cols].copy()
    manifest.insert(0, "sample_index", range(len(manifest)))
    manifest["split_placeholder"] = ""

    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
    manifest.to_csv(args.output_csv, index=False)

    n_frontal = (manifest["Frontal/Lateral"] == "Frontal").sum()
    n_non = len(manifest) - n_frontal
    print(f"Manifest written: {args.output_csv}")
    print(f"  Total: {len(manifest)}")
    print(f"  Frontal: {n_frontal}")
    print(f"  Non-frontal: {n_non}")
    print(f"  Seed: {args.seed}")
    print(f"  Unique patients: {manifest['patient_id'].nunique()}")


if __name__ == "__main__":
    main()
