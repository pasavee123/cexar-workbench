import csv
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torchxrayvision as xrv
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
CONFIGS = ROOT / "configs"
OUTPUT_CSV = ARTIFACTS / "xrv_chexpert_outputs.csv"
METRIC_JSON = ARTIFACTS / "metric_sanity.json"
CROSSWALK_MD = ARTIFACTS / "label_crosswalk.md"

VALID_CSV = Path("D:/Dataset_Chexpert/archive/valid.csv")
VALID_DIR = Path("D:/Dataset_Chexpert/archive")
SAMPLE_SIZE = 100

XRV_TO_CHEXPERT = {
    0: ("Atelectasis", "Atelectasis"),
    1: ("Consolidation", "Consolidation"),
    3: ("Pneumothorax", "Pneumothorax"),
    4: ("Edema", "Edema"),
    7: ("Effusion", "Pleural Effusion"),
    8: ("Pneumonia", "Pneumonia"),
    10: ("Cardiomegaly", "Cardiomegaly"),
    14: ("Lung Lesion", "Lung Lesion"),
    15: ("Fracture", "Fracture"),
    16: ("Lung Opacity", "Lung Opacity"),
    17: ("Enlarged Cardiomediastinum", "Enlarged Cardiomediastinum"),
}

UNMAPPED_XRV = {
    2: "Infiltration",
    5: "Emphysema",
    6: "Fibrosis",
    9: "Pleural_Thickening",
    11: "Nodule",
    12: "Mass",
    13: "Hernia",
}

CHEXPERT_PATHOLOGY_COLS = [
    "No Finding",
    "Enlarged Cardiomediastinum",
    "Cardiomegaly",
    "Lung Opacity",
    "Lung Lesion",
    "Edema",
    "Consolidation",
    "Pneumonia",
    "Atelectasis",
    "Pneumothorax",
    "Pleural Effusion",
    "Pleural Other",
    "Fracture",
    "Support Devices",
]


def compute_auroc(y_true, y_score):
    y_true = np.asarray(y_true, dtype=float)
    y_score = np.asarray(y_score, dtype=float)
    mask = ~np.isnan(y_true) & ~np.isnan(y_score)
    y_true = y_true[mask]
    y_score = y_score[mask]

    if len(y_true) == 0:
        return None, "no valid samples"
    if len(np.unique(y_true)) < 2:
        return None, "only one class present"

    desc = np.argsort(-y_score)
    y_true_sorted = y_true[desc]
    y_score_sorted = y_score[desc]

    tps = np.cumsum(y_true_sorted)
    fps = np.cumsum(1 - y_true_sorted)
    total_pos = tps[-1]
    total_neg = fps[-1]

    if total_pos == 0 or total_neg == 0:
        return None, "no positive or no negative samples"

    tpr = np.concatenate([[0], tps / total_pos, [1]])
    fpr = np.concatenate([[0], fps / total_neg, [1]])

    area = np.trapz(tpr, fpr)
    return float(area), "computed"


def load_labels():
    rows = []
    with VALID_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
    frontal = [r for r in rows if r.get("Frontal/Lateral") == "Frontal"]
    frontal.sort(key=lambda r: r["Path"])
    return frontal[:SAMPLE_SIZE]


def preprocess(image_path):
    image = Image.open(image_path).convert("L")
    image = image.resize((224, 224), Image.BILINEAR)
    array = np.asarray(image).astype("float32")
    array = xrv.datasets.normalize(array, 255)
    tensor = torch.from_numpy(array).unsqueeze(0).unsqueeze(0)
    return tensor


def resolve_image_path(label_row):
    relative = label_row["Path"]
    if relative.startswith("CheXpert-v1.0-small/"):
        relative = relative[len("CheXpert-v1.0-small/"):]
    full_path = VALID_DIR / relative
    return full_path


def parse_label(value):
    if value is None or value.strip() == "":
        return np.nan
    try:
        v = float(value)
        return v
    except ValueError:
        return np.nan


def main():
    print("Loading validation labels...")
    label_rows = load_labels()
    print(f"Selected {len(label_rows)} frontal validation images (deterministic, first {SAMPLE_SIZE} sorted by Path)")

    print("Loading TorchXRayVision DenseNet121...")
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    model.eval()
    pathologies = list(model.pathologies)
    print(f"Model pathologies ({len(pathologies)}): {pathologies}")

    print("Writing label crosswalk...")
    crosswalk_lines = [
        "# Label Crosswalk: TorchXRayVision DenseNet121 ↔ CheXpert Validation Labels",
        "",
        f"XRV pathology count: {len(pathologies)}",
        f"CheXpert validation pathology columns: {len(CHEXPERT_PATHOLOGY_COLS)}",
        "",
        "## Mapped Labels",
        "",
        "| XRV Index | XRV Pathology | CheXpert Column |",
        "|-----------|---------------|-----------------|",
    ]
    for xrv_idx, (xrv_name, chex_name) in sorted(XRV_TO_CHEXPERT.items()):
        crosswalk_lines.append(f"| {xrv_idx} | {xrv_name} | {chex_name} |")

    crosswalk_lines.extend([
        "",
        "## Unmapped XRV Pathologies (no matching CheXpert column)",
        "",
        "| XRV Index | XRV Pathology | Reason |",
        "|-----------|---------------|--------|",
    ])
    for xrv_idx, xrv_name in sorted(UNMAPPED_XRV.items()):
        crosswalk_lines.append(f"| {xrv_idx} | {xrv_name} | No corresponding column in CheXpert valid.csv |")

    unmapped_chex = set(CHEXPERT_PATHOLOGY_COLS) - {v[1] for v in XRV_TO_CHEXPERT.values()}
    crosswalk_lines.extend([
        "",
        "## Unmapped CheXpert Columns (no matching XRV pathology)",
        "",
        "| CheXpert Column |",
        "|----------------|",
    ])
    for col in sorted(unmapped_chex):
        crosswalk_lines.append(f"| {col} |")

    crosswalk_lines.append("")
    CROSSWALK_MD.write_text("\n".join(crosswalk_lines), encoding="utf-8")
    print(f"Wrote {CROSSWALK_MD}")

    print("Running inference and collecting outputs...")
    all_outputs = []
    failed = []

    with torch.no_grad():
        for i, row in enumerate(label_rows):
            img_path = resolve_image_path(row)
            if not img_path.exists():
                failed.append({"index": i, "path": str(img_path), "reason": "file not found"})
                all_outputs.append(None)
                continue
            try:
                tensor = preprocess(img_path)
                output = model(tensor).squeeze(0).tolist()
                all_outputs.append(output)
            except Exception as exc:
                failed.append({"index": i, "path": str(img_path), "reason": str(exc)})
                all_outputs.append(None)

    print(f"Inference complete. {len([o for o in all_outputs if o is not None])}/{len(label_rows)} images succeeded.")
    if failed:
        print(f"Failed: {len(failed)} images")
        for f in failed:
            print(f"  [{f['index']}] {f['path']}: {f['reason']}")

    print("Writing raw outputs CSV...")
    header = ["image_index", "PatientPath"] + pathologies
    csv_rows = [header]
    for i, (row, outputs) in enumerate(zip(label_rows, all_outputs)):
        if outputs is None:
            csv_rows.append([str(i), row["Path"]] + ["FAILED"] * len(pathologies))
        else:
            csv_rows.append([str(i), row["Path"]] + [f"{v:.6f}" for v in outputs])

    OUTPUT_CSV.write_text("\n".join(",".join(r) for r in csv_rows), encoding="utf-8")
    print(f"Wrote {OUTPUT_CSV}")

    print("Computing metric sanity check...")
    metric_results = {}

    for xrv_idx, (xrv_name, chex_col) in XRV_TO_CHEXPERT.items():
        y_true = []
        y_score = []
        for i, (row, outputs) in enumerate(zip(label_rows, all_outputs)):
            if outputs is None:
                continue
            label_val = parse_label(row.get(chex_col, ""))
            if np.isnan(label_val):
                continue
            y_true.append(label_val)
            y_score.append(outputs[xrv_idx])

        auroc, reason = compute_auroc(y_true, y_score)
        metric_results[xrv_name] = {
            "chexpert_column": chex_col,
            "xrv_index": xrv_idx,
            "num_samples": len(y_true),
            "auroc": auroc,
            "status": reason,
        }

    all_aurocs = [v["auroc"] for v in metric_results.values() if v["auroc"] is not None]
    summary = {
        "experiment": "EXP-0012-xrv-chexpert-label-crosswalk",
        "model": "densenet121-res224-all",
        "torchxrayvision_version": xrv.__version__,
        "sample_description": f"First {SAMPLE_SIZE} frontal validation images from CheXpert valid.csv (deterministic sort by Path)",
        "num_images_attempted": len(label_rows),
        "num_images_succeeded": len([o for o in all_outputs if o is not None]),
        "num_images_failed": len(failed),
        "num_mapped_labels": len(XRV_TO_CHEXPERT),
        "num_unmapped_xrv_labels": len(UNMAPPED_XRV),
        "auroc_count_computed": len(all_aurocs),
        "auroc_values": all_aurocs,
        "per_label": metric_results,
        "medical_claims": "none; this is a pipeline sanity check only, not a clinical evaluation",
        "notes": [
            "AUROC computed with local implementation (sklearn not available in venv).",
            "Only labels with both positive (1.0) and negative (0.0) examples were included.",
            "Missing/NaN labels were excluded per-label.",
            "Do not interpret these metrics as clinical performance.",
        ],
    }

    METRIC_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {METRIC_JSON}")

    if failed:
        print(f"\nWARNING: {len(failed)} images failed inference.")
        print("Experiment continues with available results.")
        return 0

    print("\nDone. Pipeline sanity check complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())