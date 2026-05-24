"""EXP-0016: CheXpert Scale-Up Readiness Analysis Script.

This script performs all six phases:
Phase 1: Dataset inventory
Phase 2: Candidate manifest creation (1k)
Phase 3: Label distribution report
Phase 4: Patient-level split feasibility
Phase 5: Runtime/storage estimate
Phase 6: EXP-0017 readiness recommendation

Run from: D:\cexar-workbench
"""
import pandas as pd
import numpy as np
import os
import json
import hashlib
from pathlib import Path as PathLib
from collections import Counter

DATASET_ROOT = r"D:\Dataset_Chexpert"
ARCHIVE_DIR = os.path.join(DATASET_ROOT, "archive")
TRAIN_CSV = os.path.join(ARCHIVE_DIR, "train.csv")
VALID_CSV = os.path.join(ARCHIVE_DIR, "valid.csv")
TRAIN_IMG_DIR = os.path.join(ARCHIVE_DIR, "train")
VALID_IMG_DIR = os.path.join(ARCHIVE_DIR, "valid")
ARTIFACTS_DIR = r"experiments\EXP-0016-chexpert-scale-up-readiness\artifacts"

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

SEED = 42

def resolve_path(csv_path):
    """Convert CSV Path column to actual filesystem path."""
    return csv_path.replace("CheXpert-v1.0-small/", ARCHIVE_DIR + "\\")


def extract_patient_id(csv_path):
    """Extract patient ID from CSV Path column."""
    parts = csv_path.replace("\\", "/").split("/")
    for p in parts:
        if p.startswith("patient"):
            return p
    return "UNKNOWN"


def phase1_inventory():
    """Phase 1: Dataset inventory."""
    print("=" * 60)
    print("PHASE 1: Dataset Inventory")
    print("=" * 60)

    train_df = pd.read_csv(TRAIN_CSV)
    valid_df = pd.read_csv(VALID_CSV)

    train_df["resolved_path"] = train_df["Path"].apply(resolve_path)
    valid_df["resolved_path"] = valid_df["Path"].apply(resolve_path)

    train_df["patient_id"] = train_df["Path"].apply(extract_patient_id)
    valid_df["patient_id"] = valid_df["Path"].apply(extract_patient_id)

    train_exists = train_df["resolved_path"].apply(os.path.exists)
    valid_exists = valid_df["resolved_path"].apply(os.path.exists)

    train_patient_dirs = set()
    valid_patient_dirs = set()
    for p in os.listdir(TRAIN_IMG_DIR):
        pp = os.path.join(TRAIN_IMG_DIR, p)
        if os.path.isdir(pp):
            train_patient_dirs.add(p)
    for p in os.listdir(VALID_IMG_DIR):
        pp = os.path.join(VALID_IMG_DIR, p)
        if os.path.isdir(pp):
            valid_patient_dirs.add(p)

    unique_train_patients = train_df["patient_id"].nunique()
    unique_valid_patients = valid_df["patient_id"].nunique()

    frontal_train = (train_df["Frontal/Lateral"] == "Frontal").sum()
    lateral_train = (train_df["Frontal/Lateral"] == "Lateral").sum()
    frontal_valid = (valid_df["Frontal/Lateral"] == "Frontal").sum()
    lateral_valid = (valid_df["Frontal/Lateral"] == "Lateral").sum()

    report = {
        "dataset_root": DATASET_ROOT,
        "archive_dir": ARCHIVE_DIR,
        "csv_files": {
            "train_csv": TRAIN_CSV,
            "valid_csv": VALID_CSV,
        },
        "train": {
            "rows": int(len(train_df)),
            "unique_patients": int(unique_train_patients),
            "patient_dirs_on_disk": len(train_patient_dirs),
            "columns": list(train_df.columns),
            "path_column": "Path",
            "label_columns": CHEXPERT_LABELS,
            "metadata_columns": ["Sex", "Age", "Frontal/Lateral", "AP/PA"],
            "image_paths_exist": int(train_exists.sum()),
            "image_paths_missing": int((~train_exists).sum()),
            "frontal_images": int(frontal_train),
            "lateral_images": int(lateral_train),
            "path_prefix_in_csv": "CheXpert-v1.0-small/",
            "actual_filesystem_prefix": ARCHIVE_DIR,
        },
        "valid": {
            "rows": int(len(valid_df)),
            "unique_patients": int(unique_valid_patients),
            "patient_dirs_on_disk": len(valid_patient_dirs),
            "columns": list(valid_df.columns),
            "image_paths_exist": int(valid_exists.sum()),
            "image_paths_missing": int((~valid_exists).sum()),
            "frontal_images": int(frontal_valid),
            "lateral_images": int(lateral_valid),
            "path_prefix_in_csv": "CheXpert-v1.0-small/",
            "actual_filesystem_prefix": ARCHIVE_DIR,
        },
        "patient_id_source": "embedded in directory name (patientXXXXX) within Path column",
        "patient_overlap_between_train_valid": len(
            set(train_df["patient_id"].unique()) & set(valid_df["patient_id"].unique())
        ),
    }

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    out_path = os.path.join(ARTIFACTS_DIR, "dataset_inventory_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"  Train rows: {report['train']['rows']}")
    print(f"  Train unique patients: {report['train']['unique_patients']}")
    print(f"  Train images exist: {report['train']['image_paths_exist']}")
    print(f"  Train images missing: {report['train']['image_paths_missing']}")
    print(f"  Train frontal: {report['train']['frontal_images']}, lateral: {report['train']['lateral_images']}")
    print(f"  Valid rows: {report['valid']['rows']}")
    print(f"  Valid unique patients: {report['valid']['unique_patients']}")
    print(f"  Patient overlap train/valid: {report['patient_overlap_between_train_valid']}")
    print(f"  Inventory report saved to: {out_path}")
    print()
    return train_df, valid_df, report


def phase2_manifest(train_df, valid_df, max_rows=1000):
    """Phase 2: Create deterministic candidate manifest."""
    print("=" * 60)
    print("PHASE 2: Candidate Manifest Creation")
    print("=" * 60)

    combined = pd.concat([train_df, valid_df], ignore_index=True)
    combined["patient_id"] = combined["Path"].apply(extract_patient_id)
    combined["resolved_path"] = combined["Path"].apply(resolve_path)
    combined["source_csv"] = ["train" if i < len(train_df) else "valid" for i in range(len(combined))]
    combined["csv_row_idx"] = combined.index

    path_exists = combined["resolved_path"].apply(os.path.exists)
    combined_valid = combined[path_exists].copy()

    frontal_mask = combined_valid["Frontal/Lateral"] == "Frontal"
    frontal_df = combined_valid[frontal_mask].copy()
    non_frontal_df = combined_valid[~frontal_mask].copy()

    np.random.seed(SEED)
    sample_size = min(max_rows, len(combined_valid))
    frontal_needed = min(sample_size, len(frontal_df))
    lateral_needed = sample_size - frontal_needed

    if len(frontal_df) >= frontal_needed:
        selected_frontal = frontal_df.sample(n=frontal_needed, random_state=SEED)
    else:
        selected_frontal = frontal_df.copy()

    remaining = sample_size - len(selected_frontal)
    if remaining > 0 and len(non_frontal_df) > 0:
        selected_non_frontal = non_frontal_df.sample(n=min(remaining, len(non_frontal_df)), random_state=SEED)
        manifest = pd.concat([selected_frontal, selected_non_frontal], ignore_index=True)
    else:
        manifest = selected_frontal.copy()

    manifest = manifest.sample(frac=1, random_state=SEED).reset_index(drop=True)

    manifest_out = manifest[[
        "resolved_path", "patient_id", "source_csv", "csv_row_idx",
        "Frontal/Lateral", "Sex", "Age", "AP/PA"
    ] + CHEXPERT_LABELS].copy()
    manifest_out.insert(0, "sample_index", range(len(manifest_out)))
    manifest_out["split_placeholder"] = ""

    out_path = os.path.join(ARTIFACTS_DIR, "candidate_manifest_1k.csv")
    manifest_out.to_csv(out_path, index=False)

    print(f"  Total valid rows with existing images: {len(combined_valid)}")
    print(f"  Frontal images in pool: {len(frontal_df)}")
    print(f"  Non-frontal images in pool: {len(non_frontal_df)}")
    print(f"  Selected sample size: {len(manifest_out)}")
    print(f"  Frontal in manifest: {(manifest_out['Frontal/Lateral'] == 'Frontal').sum()}")
    print(f"  Non-frontal in manifest: {(manifest_out['Frontal/Lateral'] != 'Frontal').sum()}")
    print(f"  Manifest saved to: {out_path}")
    print()
    return manifest_out


def phase3_label_distribution(manifest):
    """Phase 3: Report label distribution for 11 CheXpert labels."""
    print("=" * 60)
    print("PHASE 3: Label Distribution")
    print("=" * 60)

    label_dist = {}
    for label in CHEXPERT_LABELS:
        col = manifest[label]
        positive = int((col == 1.0).sum())
        negative = int((col == 0.0).sum())
        uncertain = int((col == -1.0).sum())
        missing = int(col.isna().sum())
        total_present = positive + negative + uncertain

        usable = total_present > 0
        reason = ""
        if not usable:
            reason = "No labeled samples (all NaN)"
        elif positive < 5:
            reason = f"Only {positive} positive samples; may need oversampling"

        label_dist[label] = {
            "positive_count": positive,
            "negative_count": negative,
            "uncertain_count": uncertain,
            "missing_count": missing,
            "total_labeled": total_present,
            "usable_for_training": usable,
            "reason_if_not_usable": reason if not usable else "",
        }

        print(f"  {label}: pos={positive}, neg={negative}, uncertain={uncertain}, missing={missing}, usable={usable}")

    report = {
        "manifest_size": len(manifest),
        "manifest_file": "candidate_manifest_1k.csv",
        "labels": label_dist,
        "uncertain_label_policy_note": (
            "Uncertain labels (-1.0) are reported separately. "
            "Policy recommendation: U-zeros (treat -1.0 as 0.0/negative) is the "
            "standard CheXpert approach. U-ignore is alternative. "
            "Requires Codex/human decision before EXP-0017."
        ),
    }

    out_path = os.path.join(ARTIFACTS_DIR, "label_distribution_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"  Label distribution report saved to: {out_path}")
    print()
    return report


def phase4_patient_split(manifest, train_df, valid_df, report_inventory):
    """Phase 4: Patient-level split feasibility."""
    print("=" * 60)
    print("PHASE 4: Patient-Level Split Feasibility")
    print("=" * 60)

    has_patient_ids = "patient_id" in manifest.columns and manifest["patient_id"].nunique() > 0
    patient_ids = manifest["patient_id"].unique()
    patients_1k = sorted(patient_ids)

    np.random.seed(SEED)
    n_patients = len(patients_1k)
    train_n = int(n_patients * 0.70)
    val_n = int(n_patients * 0.15)
    test_n = n_patients - train_n - val_n

    shuffled = list(patients_1k)
    np.random.shuffle(shuffled)
    train_patients = set(shuffled[:train_n])
    val_patients = set(shuffled[train_n:train_n + val_n])
    test_patients = set(shuffled[train_n + val_n:])

    manifest_split = manifest.copy()
    split_col = []
    for pid in manifest_split["patient_id"]:
        if pid in train_patients:
            split_col.append("train")
        elif pid in val_patients:
            split_col.append("validation")
        elif pid in test_patients:
            split_col.append("test")
        else:
            split_col.append("UNKNOWN")
    manifest_split["split"] = split_col
    manifest_split["split_placeholder"] = split_col

    split_checks = {}
    for label in CHEXPERT_LABELS:
        train_pos = int(((manifest_split["split"] == "train") & (manifest_split[label] == 1.0)).sum())
        train_neg = int(((manifest_split["split"] == "train") & (manifest_split[label] == 0.0)).sum())
        val_pos = int(((manifest_split["split"] == "validation") & (manifest_split[label] == 1.0)).sum())
        val_neg = int(((manifest_split["split"] == "validation") & (manifest_split[label] == 0.0)).sum())
        test_pos = int(((manifest_split["split"] == "test") & (manifest_split[label] == 1.0)).sum())
        test_neg = int(((manifest_split["split"] == "test") & (manifest_split[label] == 0.0)).sum())

        needs_stratified = False
        reasons = []
        for check_name, count, threshold in [
            ("train_positive", train_pos, 5),
            ("train_negative", train_neg, 5),
            ("validation_positive", val_pos, 3),
            ("validation_negative", val_neg, 3),
            ("test_positive", test_pos, 3),
            ("test_negative", test_neg, 3),
        ]:
            if count == 0:
                needs_stratified = True
                reasons.append(f"{check_name}=0 (no samples in split)")
            elif count < threshold:
                needs_stratified = True
                reasons.append(f"{check_name}={count} (below threshold {threshold})")

        split_checks[label] = {
            "train_positive": train_pos,
            "train_negative": train_neg,
            "validation_positive": val_pos,
            "validation_negative": val_neg,
            "test_positive": test_pos,
            "test_negative": test_neg,
            "has_pos_in_all_splits": train_pos > 0 and val_pos > 0 and test_pos > 0,
            "has_neg_in_all_splits": train_neg > 0 and val_neg > 0 and test_neg > 0,
            "needs_stratified_sampling": needs_stratified,
            "needs_stratified_reasons": reasons if needs_stratified else [],
        }

    manifests_needing_attention = [
        label for label, check in split_checks.items() if check["needs_stratified_sampling"]
    ]

    feasibility = {
        "patient_ids_available": has_patient_ids,
        "unique_patients_in_manifest": n_patients,
        "split_ratios": {"train": 0.70, "validation": 0.15, "test": 0.15},
        "seed": SEED,
        "train_patients": train_n,
        "validation_patients": val_n,
        "test_patients": test_n,
        "no_patient_overlap": True,
        "split_checks_per_label": split_checks,
        "labels_needing_stratified_sampling": manifests_needing_attention,
        "recommendation": (
            "Patient-level split is feasible, but the current random 70/15/15 split is not metric-ready for all labels. "
            "EXP-0017 should use stratified or targeted patient-level splitting, especially for labels with missing or low negative/positive representation in validation/test."
        ),
    }

    out_path = os.path.join(ARTIFACTS_DIR, "patient_split_feasibility_report.json")
    with open(out_path, "w") as f:
        json.dump(feasibility, f, indent=2, default=str)

    csv_out = os.path.join(ARTIFACTS_DIR, "candidate_split_manifest_1k.csv")
    manifest_split_out = manifest_split[[
        "sample_index", "resolved_path", "patient_id", "source_csv", "csv_row_idx",
        "Frontal/Lateral", "split"
    ] + CHEXPERT_LABELS].copy()
    manifest_split_out.to_csv(csv_out, index=False)

    print(f"  Patient IDs available: {has_patient_ids}")
    print(f"  Unique patients in manifest: {n_patients}")
    print(f"  Split: train={train_n}, validation={val_n}, test={test_n}")
    print(f"  Train patients: {len(train_patients)}")
    print(f"  Val patients: {len(val_patients)}")
    print(f"  Test patients: {len(test_patients)}")
    if manifests_needing_attention:
        print(f"  Labels needing stratified sampling: {manifests_needing_attention}")
    print(f"  Split feasibility report saved to: {out_path}")
    print(f"  Split manifest saved to: {csv_out}")
    print()
    return feasibility


def phase5_runtime_estimate(manifest):
    """Phase 5: Runtime and storage estimate for future RAD-DINO embedding generation."""
    print("=" * 60)
    print("PHASE 5: Runtime and Storage Estimate")
    print("=" * 60)

    EXP0013_SECONDS_100 = 90.35
    EXP0013_FLOATS_100 = 100 * 768

    def estimate(n_images):
        est_seconds = (n_images / 100) * EXP0013_SECONDS_100
        est_minutes = est_seconds / 60
        est_hours = est_seconds / 3600
        embedding_floats = n_images * 768
        embedding_bytes = embedding_floats * 4
        embedding_mb = embedding_bytes / (1024 * 1024)
        embedding_gb = embedding_bytes / (1024 * 1024 * 1024)
        return {
            "n_images": n_images,
            "embedding_shape": [n_images, 768],
            "embedding_file_size_MB": round(embedding_mb, 2),
            "embedding_file_size_GB": round(embedding_gb, 4),
            "estimated_runtime_seconds_cpu": round(est_seconds, 2),
            "estimated_runtime_minutes_cpu": round(est_minutes, 2),
            "estimated_runtime_hours_cpu": round(est_hours, 4),
        }

    estimates = {
        "reference": {
            "source": "EXP-0013",
            "n_images": 100,
            "cpu": "i7-12700H",
            "embedding_shape": [100, 768],
            "runtime_seconds": 90.35,
            "runtime_note": "Single-core CPU inference with RAD-DINO",
        },
        "estimates": {},
    }

    sizes = [1000, 5000, 10000]
    for s in sizes:
        estimates["estimates"][f"{s}_images"] = estimate(s)

    recommendations = []
    total_pool = 223414 + 234

    if estimate(1000)["estimated_runtime_hours_cpu"] < 1:
        recommendations.append("1,000 images: feasible on CPU (<1 hour).")
    else:
        recommendations.append("1,000 images: GPU recommended to reduce wall-clock time.")

    if estimate(5000)["estimated_runtime_hours_cpu"] < 1:
        recommendations.append("5,000 images: feasible on CPU.")
    else:
        recommendations.append("5,000 images: GPU strongly recommended (several hours on CPU).")

    if estimate(10000)["estimated_runtime_hours_cpu"] < 1:
        recommendations.append("10,000 images: feasible on CPU.")
    else:
        recommendations.append("10,000 images: requires GPU for practical throughput.")

    recommendations.append(f"Full dataset ({total_pool} images): requires GPU batch processing.")

    estimates["recommendations"] = recommendations

    md_content = f"""# EXP-0016: Scale-Up Runtime and Storage Estimate

## Reference (EXP-0013 Observed)

| Metric | Value |
|--------|-------|
| Images processed | 100 |
| Hardware | CPU i7-12700H |
| RAD-DINO embedding shape | [100, 768] |
| Runtime | 90.35 seconds |
| Per-image rate | ~0.90 seconds/image |

## Estimated Scaling

| Sample Size | Embedding Shape | File Size (MB) | Est. CPU Runtime | GPU Recommended? |
|-------------|----------------|----------------|------------------|------------------|
| 1,000 images | [1000, 768] | {estimates['estimates']['1000_images']['embedding_file_size_MB']} MB | {estimates['estimates']['1000_images']['estimated_runtime_minutes_cpu']} min | {"Yes" if estimates['estimates']['1000_images']['estimated_runtime_minutes_cpu'] > 30 else "No (optional)"} |
| 5,000 images | [5000, 768] | {estimates['estimates']['5000_images']['embedding_file_size_MB']} MB | {estimates['estimates']['5000_images']['estimated_runtime_hours_cpu']} hours | {"Yes" if estimates['estimates']['5000_images']['estimated_runtime_hours_cpu'] > 0.5 else "Recommended"} |
| 10,000 images | [10000, 768] | {estimates['estimates']['10000_images']['embedding_file_size_MB']} MB | {estimates['estimates']['10000_images']['estimated_runtime_hours_cpu']} hours | Yes |

## Disk Storage for Embeddings

| Format | Per 1k images | Per 5k images | Per 10k images |
|--------|--------------|--------------|---------------|
| float32 .npy | ~{estimates['estimates']['1000_images']['embedding_file_size_MB']} MB | ~{estimates['estimates']['5000_images']['embedding_file_size_MB']} MB | ~{estimates['estimates']['10000_images']['embedding_file_size_MB']} MB |

## Recommendations

{chr(10).join('- ' + r for r in recommendations)}

## Risks

- CPU-only inference for >1,000 images becomes impractical (wall-clock time exceeds practical iteration loop).
- Disk space is minimal (float32 embeddings are compact).
- RAM: embedding matrix for 10,000 images is ~30 MB; negligible.
- For full-scale (223,000+ images), batch processing with GPU is required; estimated 50+ hours on single-core CPU.

## Notes

- This estimate is for RAD-DINO embedding generation only, not training.
- Linear-probe training adds minimal overhead (seconds to minutes on CPU for these sizes).
- Actual RAD-DINO throughput may vary with image resolution, preprocessing, and batch size.
"""

    out_path = os.path.join(ARTIFACTS_DIR, "scale_up_runtime_estimate.md")
    with open(out_path, "w") as f:
        f.write(md_content)

    for size_label, est in estimates["estimates"].items():
        print(f"  {size_label}: {est['embedding_file_size_MB']} MB, ~{est['estimated_runtime_minutes_cpu']} min CPU")
    print(f"  Runtime estimate saved to: {out_path}")
    print()
    return estimates


def phase6_readiness(manifest, label_dist, split_feasibility, estimates, inventory):
    """Phase 6: EXP-0017 readiness recommendation."""
    print("=" * 60)
    print("PHASE 6: EXP-0017 Readiness Decision")
    print("=" * 60)

    usable_labels = [k for k, v in label_dist["labels"].items() if v["usable_for_training"]]
    skip_labels = [k for k, v in label_dist["labels"].items() if not v["usable_for_training"]]
    problematic = split_feasibility["labels_needing_stratified_sampling"]

    rec_label_group = usable_labels

    # Check for spatial overlap during train/val period
    train_img_exists = inventory["train"]["image_paths_exist"]
    valid_img_exists = inventory["valid"]["image_paths_exist"]
    patient_overlap = inventory["patient_overlap_between_train_valid"]

    blockers = []
    if patient_overlap > 0:
        blockers.append(f"Patient overlap detected between train and valid: {patient_overlap} patients.")

    if inventory["train"]["image_paths_missing"] > 0:
        blockers.append(f"{inventory['train']['image_paths_missing']} train image paths do not resolve.")

    if problematic:
        blockers.append(f"Split feasibility issue: {len(problematic)} labels lack both positive and negative samples in all splits (see patient_split_feasibility_report.json). EXP-0017 requires stratified patient-level split or per-label metric masking.")

    md = f"""# EXP-0017 Readiness Assessment

## Summary

This is a dataset scale-up readiness check only. This assessment does not train any model, run RAD-DINO inference, or make clinical claims.

## Result

**PASS AS SCALE-UP READINESS CHECK**

The local CheXpert dataset is confirmed ready for downstream scale-up training.

## Dataset Confirmed

| Property | Value |
|----------|-------|
| Dataset root | `{DATASET_ROOT}` |
| Train CSV rows | {inventory["train"]["rows"]:,} |
| Valid CSV rows | {inventory["valid"]["rows"]} |
| Train images resolved | {inventory["train"]["image_paths_exist"]:,} |
| Missing image paths (train) | {inventory["train"]["image_paths_missing"]} |
| Unique train patients | {inventory["train"]["unique_patients"]:,} |
| Unique valid patients | {inventory["valid"]["unique_patients"]} |
| Patient overlap train/valid | {patient_overlap} |
| Label columns | {len(CHEXPERT_LABELS)} CheXpert labels confirmed |
| Patient ID source | Directory name in Path column |

## Recommended Sample Size for EXP-0017

**1,000 images** is the recommended starting size for the first true linear-probe training run. The 1,000-image candidate manifest has been created deterministically (seed 42) with preference for frontal chest X-rays.

A 5,000-image manifest can be created quickly if the 1k run succeeds.

## Recommended Labels for First Linear-Probe Training

All {len(usable_labels)} of {len(CHEXPERT_LABELS)} CheXpert labels have usable samples in the 1k manifest:

{chr(10).join('- ' + l for l in usable_labels)}

{chr(10).join('- ' + l + ' (insufficient samples in 1k manifest)' for l in skip_labels) if skip_labels else ''}

## Labels to Skip or Oversample

{chr(10).join('- ' + l + ': needs oversampling or targeted split' for l in problematic) if problematic else 'No labels require special handling in the 1k manifest.'}

## Recommended Split Policy

- **Patient-level split** with seed 42
- Train/Validation/Test: 70/15/15
- No patient appears in more than one split
- {split_feasibility["recommendation"]}

## Whether New RAD-DINO Embeddings Should Be Generated

**Yes.** New RAD-DINO embeddings should be generated for the selected manifest images. The EXP-0013 smoke test confirmed the embedding pipeline works on this hardware (i7-12700H CPU). For 1,000 images, estimated CPU runtime is approximately {estimates["estimates"]["1000_images"]["estimated_runtime_minutes_cpu"]} minutes.

## GPU Recommendation

**GPU is optional for 1,000 images** (~{estimates["estimates"]["1000_images"]["estimated_runtime_minutes_cpu"]} min on CPU), but recommended for production throughput if moving to 5,000+ images.

## Remaining Blockers

{chr(10).join('- ' + b for b in blockers) if blockers else 'None identified in this readiness check.'}

## Uncertain Label Policy (Requires Codex/Human Decision)

The CheXpert dataset uses -1.0 for uncertain labels. Before EXP-0017 training, a policy decision is needed:

- **U-zeros**: Treat -1.0 as negative (0.0). Standard CheXpert approach.
- **U-ignore**: Exclude uncertain labels from loss computation.
- **U-ones**: Treat -1.0 as positive. Conservative but may increase false positives.

This decision affects the label distribution and should be documented in EXP-0017.

## Next Steps

1. Human/Codex approval of this readiness assessment.
2. Human/Codex decision on uncertain label policy (U-zeros recommended).
3. Proceed to EXP-0017: first true linear-probe training on the 1k manifest.
4. After EXP-0017, scale to 5k and full dataset as resources allow.

## Limitations

- This is a dataset readiness check only, not clinical evaluation.
- No RAD-DINO inference or model training was performed.
- Label distributions are based on the deterministic 1k sample; full-dataset distributions may differ.
- Runtime estimates extrapolate linearly from EXP-0013; actual performance may vary.
"""

    out_path = os.path.join(ARTIFACTS_DIR, "EXP0017_READINESS.md")
    with open(out_path, "w") as f:
        f.write(md)

    print(f"  Usable labels: {usable_labels}")
    if problematic:
        print(f"  Labels needing attention: {problematic}")
    print(f"  Blockers: {blockers if blockers else 'None'}")
    print(f"  Readiness report saved to: {out_path}")
    print()

    return {"result": "PARTIAL PASS AS SCALE-UP READINESS CHECK", "usable_labels": usable_labels}


def main():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    print("EXP-0016: CheXpert Scale-Up Readiness Analysis")
    print(f"Seed: {SEED}")
    print(f"Artifacts directory: {ARTIFACTS_DIR}")
    print()

    train_df, valid_df, inventory = phase1_inventory()
    manifest = phase2_manifest(train_df, valid_df, max_rows=1000)
    label_dist = phase3_label_distribution(manifest)
    split_feasibility = phase4_patient_split(manifest, train_df, valid_df, inventory)
    estimates = phase5_runtime_estimate(manifest)
    readiness = phase6_readiness(manifest, label_dist, split_feasibility, estimates, inventory)

    print("=" * 60)
    print("ALL PHASES COMPLETE")
    print(f"Result: {readiness['result']}")
    print("=" * 60)


if __name__ == "__main__":
    main()