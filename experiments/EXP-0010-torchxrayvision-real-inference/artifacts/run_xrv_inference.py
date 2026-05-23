import json
from pathlib import Path

import torch
import torchxrayvision as xrv


ARTIFACT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = ARTIFACT_DIR / "xrv_inference_results.json"


def main():
    torch.manual_seed(10)

    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    model.eval()

    results = []
    with torch.no_grad():
        for idx in range(5):
            image = torch.empty(1, 1, 224, 224).uniform_(-1024.0, 1024.0)
            output = model(image)
            results.append(
                {
                    "input_id": f"synthetic_{idx:03d}",
                    "input_type": "synthetic_hu_range_tensor",
                    "shape": list(image.shape),
                    "input_min": float(image.min().item()),
                    "input_max": float(image.max().item()),
                    "logits": [float(value) for value in output.squeeze(0).tolist()],
                }
            )

    payload = {
        "model": "densenet121-res224-all",
        "torchxrayvision_version": xrv.__version__,
        "data_mode": "synthetic",
        "num_images": len(results),
        "pathologies": list(model.pathologies),
        "results": results,
        "medical_claims": "none; synthetic tensors only",
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"num_images={len(results)}")
    print(f"pathology_count={len(model.pathologies)}")


if __name__ == "__main__":
    main()
