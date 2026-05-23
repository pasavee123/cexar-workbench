import csv
import json
from pathlib import Path

import numpy as np
import torch
import torchxrayvision as xrv
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
IMAGE_DIR = ARTIFACTS / "test_images"
LABELS_PATH = ARTIFACTS / "sample_labels.csv"
OUTPUT_PATH = ARTIFACTS / "xrv_real_inference_results.json"


def load_labels():
    if not LABELS_PATH.exists():
        return []
    rows = []
    with LABELS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
    return rows


def preprocess(path):
    image = Image.open(path).convert("L")
    image = image.resize((224, 224), Image.BILINEAR)
    array = np.asarray(image).astype("float32")
    array = xrv.datasets.normalize(array, 255)
    tensor = torch.from_numpy(array).unsqueeze(0).unsqueeze(0)
    return tensor, {
        "shape": list(tensor.shape),
        "input_min": float(tensor.min().item()),
        "input_max": float(tensor.max().item()),
    }


def main():
    labels = load_labels()
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    model.eval()

    results = []
    with torch.no_grad():
        for idx, image_path in enumerate(sorted(IMAGE_DIR.glob("*.jpg"))):
            tensor, stats = preprocess(image_path)
            output = model(tensor).squeeze(0)
            original_name = image_path.name.split("_", 1)[-1]
            label_row = labels[idx] if idx < len(labels) else {}
            results.append(
                {
                    "copied_filename": image_path.name,
                    "original_filename": original_name,
                    "preprocess": stats,
                    "chexpert_label_row_if_available": label_row,
                    "xrv_outputs": [float(value) for value in output.tolist()],
                }
            )

    payload = {
        "model": "densenet121-res224-all",
        "torchxrayvision_version": xrv.__version__,
        "data_mode": "real_chexpert_sample",
        "num_images": len(results),
        "pathologies": list(model.pathologies),
        "results": results,
        "medical_claims": "none; technical inference smoke test only",
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"num_images={len(results)}")
    print(f"pathology_count={len(model.pathologies)}")


if __name__ == "__main__":
    main()
