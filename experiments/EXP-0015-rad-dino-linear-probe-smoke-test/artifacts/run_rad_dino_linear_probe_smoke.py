import csv
import json
import os
import sys
import warnings

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ARTIFACTS_DIR = os.path.join(BASE, "experiments", "EXP-0015-rad-dino-linear-probe-smoke-test", "artifacts")
MANIFEST_PATH = os.path.join(BASE, "experiments", "EXP-0012B-xrv-stratified-metric-fix", "artifacts", "sample_manifest.csv")
EMBEDDINGS_PATH = os.path.join(BASE, "experiments", "EXP-0013-rad-dino-foundation-embedding-smoke", "artifacts", "rad_dino_embeddings.npz")
SUMMARY_PATH = os.path.join(BASE, "experiments", "EXP-0013-rad-dino-foundation-embedding-smoke", "artifacts", "rad_dino_embedding_summary.json")
SEED = 42
TRAIN_FRACTION = 0.8

CHEXPERT_LABELS = [
    "Atelectasis", "Consolidation", "Pneumothorax", "Edema",
    "Pleural Effusion", "Pneumonia", "Cardiomegaly", "Lung Lesion",
    "Fracture", "Lung Opacity", "Enlarged Cardiomediastinum"
]

os.makedirs(ARTIFACTS_DIR, exist_ok=True)


def validate_inputs():
    print("=== PHASE 1: Artifact Availability and Shape Check ===")
    results = {"phase": "input_validation", "status": "pending", "checks": []}

    if not os.path.exists(MANIFEST_PATH):
        results["status"] = "failed"
        results["checks"].append({"check": "manifest_exists", "passed": False, "detail": "sample_manifest.csv not found"})
        return results, None, None
    results["checks"].append({"check": "manifest_exists", "passed": True})

    if not os.path.exists(EMBEDDINGS_PATH):
        results["status"] = "failed"
        results["checks"].append({"check": "embeddings_exists", "passed": False, "detail": "rad_dino_embeddings.npz not found"})
        return results, None, None
    results["checks"].append({"check": "embeddings_exists", "passed": True})

    if not os.path.exists(SUMMARY_PATH):
        results["status"] = "failed"
        results["checks"].append({"check": "summary_exists", "passed": False, "detail": "rad_dino_embedding_summary.json not found"})
        return results, None, None
    results["checks"].append({"check": "summary_exists", "passed": True})

    with open(MANIFEST_PATH, "r") as f:
        reader = csv.DictReader(f)
        manifest_rows = list(reader)
    num_rows = len(manifest_rows)
    results["checks"].append({"check": "manifest_100_rows", "passed": num_rows == 100, "detail": f"Got {num_rows} rows, expected 100"})
    if num_rows != 100:
        results["status"] = "failed"
        return results, None, None

    manifest_indices = [int(row["sample_index"]) for row in manifest_rows]
    expected_indices = list(range(100))
    indices_ok = manifest_indices == expected_indices
    results["checks"].append({"check": "manifest_indices_sequential", "passed": indices_ok, "detail": f"Indices: {manifest_indices[:5]}...{manifest_indices[-5:]}"})
    if not indices_ok:
        results["status"] = "failed"
        return results, None, None

    with open(SUMMARY_PATH, "r") as f:
        summary = json.load(f)
    attempted = summary.get("images_attempted")
    succeeded = summary.get("images_succeeded")
    summary_ok = (attempted == 100 and succeeded == 100)
    results["checks"].append({"check": "summary_100_attempted_100_succeeded", "passed": summary_ok, "detail": f"attempted={attempted}, succeeded={succeeded}"})
    if not summary_ok:
        results["status"] = "failed"
        return results, None, None

    embeddings_data = np.load(EMBEDDINGS_PATH, allow_pickle=True)
    emb_shape = embeddings_data["embeddings"].shape
    shape_ok = emb_shape == (100, 768)
    results["checks"].append({"check": "embeddings_shape_100_768", "passed": shape_ok, "detail": f"shape={emb_shape}"})
    if not shape_ok:
        results["status"] = "failed"
        return results, None, None

    if "indices" in embeddings_data:
        emb_indices = embeddings_data["indices"].tolist()
        idx_align = emb_indices == expected_indices
        results["checks"].append({"check": "embedding_indices_align", "passed": idx_align, "detail": f"Embedding indices: {emb_indices[:5]}...{emb_indices[-5:]}"})
    else:
        results["checks"].append({"check": "embedding_indices_align", "passed": True, "detail": "No explicit indices key; assuming row-order alignment with manifest"})

    embeddings = embeddings_data["embeddings"]
    results["status"] = "passed"
    print("  PASSED: All input validation checks passed.")
    return results, manifest_rows, embeddings


def build_label_feasibility(manifest_rows):
    print("=== PHASE 2: Label Feasibility Report ===")
    report = {"phase": "label_feasibility", "labels": {}, "summary": {}}
    n = len(manifest_rows)

    for label in CHEXPERT_LABELS:
        vals = []
        for row in manifest_rows:
            raw = row.get(label, "").strip()
            if raw in ("", "NaN", "nan", "None", "null"):
                vals.append(None)
                continue
            try:
                v = float(raw)
                if v in (0.0, 1.0):
                    vals.append(int(v))
                else:
                    vals.append(None)
            except ValueError:
                vals.append(None)

        pos = sum(1 for v in vals if v == 1)
        neg = sum(1 for v in vals if v == 0)
        miss = sum(1 for v in vals if v is None)
        usable = False
        reason = ""
        if pos >= 1 and neg >= 1:
            usable = True
            reason = "Both positive and negative examples present"
        elif pos == 0:
            usable = False
            reason = "No positive examples"
        elif neg == 0:
            usable = False
            reason = "No negative examples"
        else:
            usable = False
            reason = "Insufficient samples"

        report["labels"][label] = {
            "positive_count": pos,
            "negative_count": neg,
            "missing_count": miss,
            "usable_for_smoke_training": usable,
            "reason": reason
        }
        print(f"  {label}: pos={pos} neg={neg} miss={miss} usable={usable}")

    usable_labels = [l for l, d in report["labels"].items() if d["usable_for_smoke_training"]]
    skipped_labels = [l for l, d in report["labels"].items() if not d["usable_for_smoke_training"]]
    report["summary"] = {
        "total_labels": len(CHEXPERT_LABELS),
        "usable_labels": len(usable_labels),
        "skipped_labels": len(skipped_labels),
        "usable_label_names": usable_labels,
        "skipped_label_names": skipped_labels
    }
    if not usable_labels:
        print("  STOP: No label is usable for smoke training.")
    else:
        print(f"  Usable labels: {usable_labels}")
        print(f"  Skipped labels: {skipped_labels}")
    return report


def extract_patient_id(path_str):
    parts = path_str.replace("\\", "/").split("/")
    for p in parts:
        if p.startswith("patient"):
            return p
    return None


def create_deterministic_split(manifest_rows):
    print("=== PHASE 3: Deterministic Split ===")
    rng = np.random.RandomState(SEED)
    n = len(manifest_rows)

    patient_ids = [extract_patient_id(row["Path"]) for row in manifest_rows]
    unique_patients = sorted(set(pid for pid in patient_ids if pid is not None))
    patient_to_indices = {}
    for i, pid in enumerate(patient_ids):
        patient_to_indices.setdefault(pid, []).append(i)

    if len(unique_patients) < 2:
        print("  WARNING: Fewer than 2 unique patients; using sample-level split.")
        patient_level_split = False
        idx_shuffled = list(range(n))
        rng.shuffle(idx_shuffled)
        n_train = int(n * TRAIN_FRACTION)
        train_idx = sorted(idx_shuffled[:n_train])
        eval_idx = sorted(idx_shuffled[n_train:])
    else:
        patient_level_split = True
        rng.shuffle(unique_patients)
        n_train_patients = max(1, int(len(unique_patients) * TRAIN_FRACTION))
        train_patients = set(unique_patients[:n_train_patients])
        eval_patients = set(unique_patients[n_train_patients:])
        train_idx = sorted([i for i in range(n) if patient_ids[i] in train_patients])
        eval_idx = sorted([i for i in range(n) if patient_ids[i] in eval_patients])

    output_path = os.path.join(ARTIFACTS_DIR, "split_manifest.csv")
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_index", "split", "patient_id"])
        for i in train_idx:
            writer.writerow([i, "train", patient_ids[i] if patient_ids and i < len(patient_ids) else ""])
        for i in eval_idx:
            writer.writerow([i, "eval", patient_ids[i] if patient_ids and i < len(patient_ids) else ""])

    print(f"  Split: train={len(train_idx)} eval={len(eval_idx)} patient_level={patient_level_split}")
    print(f"  Train indices: {train_idx[:10]}...{train_idx[-5:]}")
    print(f"  Eval indices: {eval_idx[:10]}...{eval_idx[-5:]}")
    return train_idx, eval_idx, unique_patients, patient_level_split


def train_probe(manifest_rows, embeddings, train_idx, eval_idx):
    print("=== PHASE 4: Linear Probe Smoke Test ===")
    metrics = {
        "phase": "probe_smoke_test",
        "pipeline_sanity_note": "PIPELINE SANITY ONLY - NOT CLINICAL PERFORMANCE",
        "config": {
            "classifier": "sklearn.linear_model.LogisticRegression",
            "seed": SEED,
            "max_iter": 1000,
            "train_fraction": TRAIN_FRACTION,
            "train_samples": len(train_idx),
            "eval_samples": len(eval_idx),
            "embedding_dim": 768,
            "device": "cpu"
        },
        "per_label_results": {},
        "summary": {}
    }

    X_train_arr = embeddings[train_idx]
    X_eval_arr = embeddings[eval_idx]

    for label in CHEXPERT_LABELS:
        print(f"\n  --- Label: {label} ---")
        y_all = []
        for row in manifest_rows:
            raw = row.get(label, "").strip()
            if raw in ("", "NaN", "nan", "None", "null"):
                y_all.append(None)
                continue
            try:
                v = float(raw)
                if v in (0.0, 1.0):
                    y_all.append(int(v))
                else:
                    y_all.append(None)
            except ValueError:
                y_all.append(None)

        y_train_full = [y_all[i] for i in train_idx]
        y_eval_full = [y_all[i] for i in eval_idx]

        train_valid_mask = [v is not None for v in y_train_full]
        eval_valid_mask = [v is not None for v in y_eval_full]

        X_train = X_train_arr[train_valid_mask]
        y_train = [y_train_full[i] for i in range(len(y_train_full)) if train_valid_mask[i]]
        X_eval = X_eval_arr[eval_valid_mask]
        y_eval = [y_eval_full[i] for i in range(len(y_eval_full)) if eval_valid_mask[i]]

        train_pos = sum(1 for v in y_train if v == 1)
        train_neg = sum(1 for v in y_train if v == 0)
        eval_pos = sum(1 for v in y_eval if v == 1)
        eval_neg = sum(1 for v in y_eval if v == 0)

        result = {
            "label": label,
            "train_positive": train_pos,
            "train_negative": train_neg,
            "train_total": train_pos + train_neg,
            "eval_positive": eval_pos,
            "eval_negative": eval_neg,
            "eval_total": eval_pos + eval_neg,
            "auroc": None,
            "status": "skipped",
            "reason": ""
        }

        if train_pos == 0 or train_neg == 0:
            result["reason"] = f"No positive ({train_pos}) or negative ({train_neg}) examples in train set"
            metrics["per_label_results"][label] = result
            print(f"    SKIPPED: {result['reason']}")
            continue
        if eval_pos == 0 or eval_neg == 0:
            result["reason"] = f"Only one class in eval set (pos={eval_pos}, neg={eval_neg})"
            metrics["per_label_results"][label] = result
            print(f"    SKIPPED: {result['reason']}")
            continue

        clf = LogisticRegression(
            random_state=SEED,
            max_iter=1000,
            solver="lbfgs",
            class_weight="balanced"
        )
        clf.fit(X_train, y_train)
        y_prob = clf.predict_proba(X_eval)[:, 1]
        auroc = float(roc_auc_score(y_eval, y_prob))

        result["auroc"] = auroc
        result["status"] = "completed"
        result["reason"] = ""
        metrics["per_label_results"][label] = result
        print(f"    AUROC={auroc:.4f} (train: {train_pos}+/{train_neg}-, eval: {eval_pos}+/{eval_neg}-)")

    completed = [l for l, r in metrics["per_label_results"].items() if r["status"] == "completed"]
    skipped = [l for l, r in metrics["per_label_results"].items() if r["status"] == "skipped"]
    metrics["summary"] = {
        "labels_tested": len(completed),
        "labels_skipped": len(skipped),
        "completed_labels": completed,
        "skipped_labels": skipped
    }
    return metrics


def main():
    validation_report, manifest_rows, embeddings = validate_inputs()
    validation_path = os.path.join(ARTIFACTS_DIR, "input_validation_report.json")
    with open(validation_path, "w") as f:
        json.dump(validation_report, f, indent=2, default=str)
    print(f"\n  Wrote: {validation_path}")

    if validation_report["status"] != "passed":
        print("\n  STOP: Input validation failed. See input_validation_report.json.")
        sys.exit(1)

    label_report = build_label_feasibility(manifest_rows)
    label_path = os.path.join(ARTIFACTS_DIR, "label_feasibility_report.json")
    with open(label_path, "w") as f:
        json.dump(label_report, f, indent=2)
    print(f"\n  Wrote: {label_path}")

    usable = [l for l, d in label_report["labels"].items() if d["usable_for_smoke_training"]]
    if not usable:
        print("\n  STOP: No usable labels. Cannot proceed to split/probe.")
        sys.exit(1)

    train_idx, eval_idx, unique_patients, patient_level_split = create_deterministic_split(manifest_rows)
    print(f"\n  Wrote: {os.path.join(ARTIFACTS_DIR, 'split_manifest.csv')}")

    probe_metrics = train_probe(manifest_rows, embeddings, train_idx, eval_idx)
    probe_path = os.path.join(ARTIFACTS_DIR, "probe_smoke_metrics.json")
    with open(probe_path, "w") as f:
        json.dump(probe_metrics, f, indent=2)
    print(f"\n  Wrote: {probe_path}")

    completed = probe_metrics["summary"]["labels_tested"]
    skipped = probe_metrics["summary"]["labels_skipped"]
    print(f"\n  Summary: {completed} labels completed, {skipped} labels skipped.")
    if completed > 0:
        print("  At least one label completed the smoke probe — pipeline contract validated.")
    else:
        print("  WARNING: No label completed the smoke probe.")

    print(f"\n  Patients split: {unique_patients} (patient_level_split={patient_level_split})")


if __name__ == "__main__":
    main()