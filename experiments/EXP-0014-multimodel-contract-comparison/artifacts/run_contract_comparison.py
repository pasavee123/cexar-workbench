import csv
import json
import os
import sys
from datetime import datetime, timezone, timedelta

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTIFACTS_DIR = os.path.dirname(os.path.abspath(__file__))

EXP12B = os.path.join(BASE, "EXP-0012B-xrv-stratified-metric-fix", "artifacts")
EXP13 = os.path.join(BASE, "EXP-0013-rad-dino-foundation-embedding-smoke", "artifacts")

MANIFEST_CSV      = os.path.join(EXP12B, "sample_manifest.csv")
XRV_OUTPUTS_CSV   = os.path.join(EXP12B, "xrv_chexpert_outputs.csv")
METRIC_SANITY_JSON = os.path.join(EXP12B, "metric_sanity.json")
RD_SUMMARY_JSON   = os.path.join(EXP13, "rad_dino_embedding_summary.json")
RD_EMBEDDINGS_NPZ = os.path.join(EXP13, "rad_dino_embeddings.npz")

TZ = timezone(timedelta(hours=7))
TS = datetime.now(TZ).isoformat()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    return headers, rows

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def file_exists(path):
    return os.path.isfile(path)

# ---------------------------------------------------------------------------
# Phase 1: Artifact availability
# ---------------------------------------------------------------------------
availability = {
    "sample_manifest.csv":    file_exists(MANIFEST_CSV),
    "xrv_chexpert_outputs.csv": file_exists(XRV_OUTPUTS_CSV),
    "metric_sanity.json":     file_exists(METRIC_SANITY_JSON),
    "rad_dino_embedding_summary.json": file_exists(RD_SUMMARY_JSON),
    "rad_dino_embeddings.npz": file_exists(RD_EMBEDDINGS_NPZ),
}
all_present = all(availability.values())

if not all_present:
    missing = [k for k, v in availability.items() if not v]
    print(f"ERROR: Missing required artifacts: {missing}", file=sys.stderr)
    sys.exit(1)

print("Phase 1 PASS: All required artifacts present.")

# ---------------------------------------------------------------------------
# Phase 2: Sample alignment
# ---------------------------------------------------------------------------
manifest_headers, manifest_rows = read_csv(MANIFEST_CSV)
xrv_headers, xrv_rows = read_csv(XRV_OUTPUTS_CSV)
rd_summary = read_json(RD_SUMMARY_JSON)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

n_manifest     = len(manifest_rows)
n_xrv          = len(xrv_rows)
n_rd_attempted = rd_summary.get("images_attempted", None)
n_rd_succeeded = rd_summary.get("images_succeeded", None)
rd_shape       = rd_summary.get("embedding_shape", None)

manifest_sample_indices = [r[0] for r in manifest_rows]
xrv_image_indices       = [r[0] for r in xrv_rows]

mismatches = []
alignment_status = "unknown"

if n_manifest != 100:
    mismatches.append(f"sample_manifest.csv has {n_manifest} rows, expected 100")
if n_xrv != 100:
    mismatches.append(f"xrv_chexpert_outputs.csv has {n_xrv} rows, expected 100")
if n_rd_attempted != 100:
    mismatches.append(f"rad_dino attempted {n_rd_attempted}, expected 100")
if n_rd_succeeded != 100:
    mismatches.append(f"rad_dino succeeded {n_rd_succeeded}, expected 100")

manifest_indices_int = [int(i) for i in manifest_sample_indices]
xrv_indices_int = [int(i) for i in xrv_image_indices]
if manifest_indices_int != list(range(100)):
    mismatches.append("sample_manifest.csv indices not sequential 0-99")
if xrv_indices_int != list(range(100)):
    mismatches.append("xrv_chexpert_outputs.csv indices not sequential 0-99")
if manifest_indices_int != xrv_indices_int:
    mismatches.append("sample_manifest and xrv_outputs indices do not match")

rd_embedding_shape = None
rd_indices_match = None
if HAS_NUMPY and file_exists(RD_EMBEDDINGS_NPZ):
    npz = np.load(RD_EMBEDDINGS_NPZ)
    embs = npz["embeddings"]
    idxs = npz["indices"]
    rd_embedding_shape = list(embs.shape)
    rd_indices_list = idxs.tolist()

    if embs.shape != (100, 768):
        mismatches.append(f"rad_dino embeddings shape {embs.shape}, expected (100, 768)")
    else:
        if rd_shape != [100, 768]:
            mismatches.append(f"summary reports shape {rd_shape}, but npz is [100, 768]")

    if rd_indices_list != list(range(100)):
        mismatches.append("rad_dino embedding indices not sequential 0-99")
    else:
        rd_indices_match = True

    if rd_indices_list != manifest_indices_int:
        mismatches.append("rad_dino indices do not align with sample_manifest indices")
    elif rd_indices_list == manifest_indices_int:
        rd_indices_match = True

elif HAS_NUMPY and not file_exists(RD_EMBEDDINGS_NPZ):
    mismatches.append("rad_dino_embeddings.npz missing even though summary reports it")
else:
    mismatches.append("numpy not available; could not verify npz shape or indices")

if not mismatches:
    alignment_status = "matched"
    print("Phase 2 PASS: Sample alignment verified (100 images across all artifacts).")
else:
    alignment_status = "mismatch"
    print(f"Phase 2 PARTIAL: Alignment issues found: {mismatches}")

sample_alignment = {
    "experiment": "EXP-0014",
    "timestamp": TS,
    "sample_count_manifest": n_manifest,
    "xrv_output_count": n_xrv,
    "rad_dino_attempted": n_rd_attempted,
    "rad_dino_succeeded": n_rd_succeeded,
    "rad_dino_embedding_shape_from_summary": rd_shape,
    "rad_dino_embedding_shape_from_npz": rd_embedding_shape,
    "indices_aligned": rd_indices_match,
    "manifest_indices": manifest_indices_int,
    "alignment_status": alignment_status,
    "mismatches": mismatches,
    "sample_source": "EXP-0012B deterministic random seed=42, 100 frontal CheXpert validation",
}
with open(os.path.join(ARTIFACTS_DIR, "sample_alignment_report.json"), "w", encoding="utf-8") as f:
    json.dump(sample_alignment, f, indent=2, default=str)

# ---------------------------------------------------------------------------
# Phase 3: Output contract comparison
# ---------------------------------------------------------------------------
xrv_pathology_count = len(xrv_headers) - 2   # subtract image_index, PatientPath
xrv_pathology_labels = xrv_headers[2:]       # 18 XRV pathologies
xrv_mapped_labels = 11                       # from EXP-0012B RESULT.md
xrv_auroc_count = 9                          # from EXP-0012B RESULT.md
xrv_skipped = 2                              # Lung Lesion, Fracture - only one class

# Read metric_sanity for richer data
try:
    metric_data = read_json(METRIC_SANITY_JSON)
except Exception:
    metric_data = {}

contract_comparison = {
    "experiment": "EXP-0014",
    "timestamp": TS,
    "models": [
        {
            "model_id": "densenet121-res224-all (TorchXRayVision 1.4.0)",
            "model_family": "supervised_chest_xray_classifier",
            "source_experiment": "EXP-0012B",
            "output_type": "per-class pathology logit scores",
            "output_shape": [100, 18],
            "label_space": {
                "type": "explicit pathology labels",
                "count": xrv_pathology_count,
                "labels": xrv_pathology_labels,
                "mapped_to_chexpert": xrv_mapped_labels,
                "unmapped_count": len(xrv_pathology_labels) - xrv_mapped_labels,
                "auroc_computed_for": xrv_auroc_count,
                "skipped_count": xrv_skipped,
                "skipped_labels": ["Lung Lesion", "Fracture"],
                "skipped_reason": "only one class in sample",
            },
            "can_compute_direct_metrics": True,
            "metric_type": "AUROC per label (pipeline sanity only)",
            "direct_chexpert_mapping": "partial (11 of 18 XRV labels)",
            "requires_downstream_head": False,
            "clinical_claims_allowed": False,
        },
        {
            "model_id": "microsoft/rad-dino",
            "model_family": "foundation_image_encoder",
            "source_experiment": "EXP-0013",
            "output_type": "image embeddings (frozen backbone)",
            "output_shape": [100, 768],
            "embedding_dim": 768,
            "label_space": {
                "type": "none",
                "count": 0,
                "labels": [],
                "mapped_to_chexpert": 0,
                "note": "No label space; requires downstream head/probe for classification",
            },
            "can_compute_direct_metrics": False,
            "metric_type": "none applicable without downstream head",
            "direct_chexpert_mapping": "none",
            "requires_downstream_head": True,
            "downstream_head_note": "Linear probe, MLP, or specialized classifier needed",
            "clinical_claims_allowed": False,
            "embedding_stats_from_npz": {
                "shape": [100, 768],
                "dtype": "float32",
                "min": None,
                "max": None,
                "mean": None,
            } if not HAS_NUMPY else {
                "shape": [100, 768],
                "dtype": "float32",
                "min": float(npz["embeddings"].min()),
                "max": float(npz["embeddings"].max()),
                "mean": float(npz["embeddings"].mean()),
            },
        },
    ],
    "key_differences": {
        "xrv_classifier": "Produces pathology scores per class; output is directly interpretable as disease likelihood",
        "rad_dino_encoder": "Produces generic image embeddings; no disease semantics without downstream training",
        "metric_readiness": "XRV can compute per-label AUROC; RAD-DINO requires a separate classification head",
        "label_dependency": "XRV has a fixed label space; RAD-DINO has no label space",
        "downstream_flexibility": "RAD-DINO embeddings can serve any downstream task; XRV is locked to chest X-ray pathology classification",
        "contract_compatibility": "These models cannot share a metric evaluation contract; they need separate adapter contracts",
    },
    "medical_claims_note": "No clinical claims are made. This is a structural contract comparison only.",
}
with open(os.path.join(ARTIFACTS_DIR, "model_output_contract_comparison.json"), "w", encoding="utf-8") as f:
    json.dump(contract_comparison, f, indent=2, default=str)

# ---------------------------------------------------------------------------
# Phase 4: CeXaR adapter contract draft
# ---------------------------------------------------------------------------
quoted_labels = ", ".join('"' + l + '"' for l in xrv_pathology_labels)
mapped_labels_list = ['Atelectasis', 'Consolidation', 'Pneumothorax', 'Edema', 'Effusion', 'Pneumonia', 'Cardiomegaly', 'Lung Lesion', 'Fracture', 'Lung Opacity', 'Enlarged Cardiomediastinum']
unmapped_labels_list = [l for l in xrv_pathology_labels if l not in mapped_labels_list]
quoted_unmapped = ", ".join('"' + l + '"' for l in unmapped_labels_list)

adapter_md = f"""# CeXaR Model Adapter Contract (Draft)

> Generated: {TS}
> Experiment: EXP-0014 (multi-model contract comparison)
>
> **Status: DRAFT** — not for production integration.
> This contract is based on read-only comparison of EXP-0012B and EXP-0013 artifacts.

---

## 1. Purpose

This document defines a generic adapter contract that can represent both classifier models (XRV DenseNet121) and embedding backbones (RAD-DINO) in the CeXaR evaluation framework. The contract ensures that downstream tooling knows the output type, shape, label semantics, and metric capabilities before attempting evaluation.

---

## 2. Contract Schema

### 2.1 Core Identity

| Field | Type | Description |
|-------|------|-------------|
| `model_id` | string | Model identifier (e.g. `densenet121-res224-all`, `microsoft/rad-dino`) |
| `model_family` | enum: `supervised_classifier`, `foundation_encoder`, `segmentation`, `detection`, `other` | Architectural family |
| `framework` | string | Inference framework (e.g. `torchxrayvision`, `transformers`, `timm`) |
| `checkpoint_source` | string | Hub ID, local path, or download URL |
| `source_experiment` | string | Experiment that first validated this model in CeXaR |

### 2.2 Input Contract

| Field | Type | Description |
|-------|------|-------------|
| `input_manifest` | string | Path to manifest CSV with image paths and optional labels |
| `num_images` | int | Number of images in the input manifest |
| `input_modality` | enum: `chest_xray`, `ct`, `mri`, `fundus`, `other` | Imaging modality |
| `preprocessing_contract` | object | Resize, normalization, channel order, augmentation details |
| `preprocessing_contract.target_size` | [int, int] | Target image dimensions (H, W) |
| `preprocessing_contract.normalization` | object | Mean/std or custom normalization |
| `preprocessing_contract.output_range` | string | Expected output value range |

### 2.3 Output Contract

| Field | Type | Description |
|-------|------|-------------|
| `output_type` | enum: `logits`, `probabilities`, `embeddings`, `segmentation_mask`, `bounding_box`, `other` | Type of model output |
| `output_shape` | [int, int] or [int, ...] | Output tensor shape per image |
| `output_dtype` | string | e.g. `float32`, `float16` |
| `embedding_dim` | int or null | Dimension of embeddings (null for non-embedding models) |
| `label_space` | object or null | Label definitions (null for embedding models) |
| `label_space.type` | string | `explicit`, `mapped`, `none` |
| `label_space.count` | int | Number of output dimensions/labels |
| `label_space.labels` | [string] | Ordered label names |
| `label_space.mapped_to_target` | [string] or int | Cross-walk to target label schema (e.g. CheXpert) |
| `requires_downstream_head` | bool | Whether classification needs an additional trained head |
| `downstream_head_description` | string or null | What kind of head is needed |

### 2.4 Metric Capabilities

| Field | Type | Description |
|-------|------|-------------|
| `can_compute_direct_metrics` | bool | Whether per-sample outputs can be directly evaluated against labels |
| `supported_metrics` | [string] | Metrics that can be computed directly (e.g. `["auroc", "auprc", "f1"]`) |
| `metric_prerequisites` | [string] or null | What must be done before metrics are computable |

### 2.5 Safety And Compliance

| Field | Type | Description |
|-------|------|-------------|
| `clinical_claims_allowed` | bool | Always `false` at experiment level |
| `medical_evaluation_readiness` | enum: `not_ready`, `sanity_only`, `requires_validation`, `external_validation_pending` | Readiness level |
| `known_limitations` | [string] | List of documented limitations |

### 2.6 Artifact Inventory

| Field | Type | Description |
|-------|------|-------------|
| `artifact_paths` | object | Map of artifact names to relative paths |
| `artifact_paths.manifest` | string | Path to sample manifest |
| `artifact_paths.outputs` | string | Path to model output file |
| `artifact_paths.metrics` | string or null | Path to metric results |
| `artifact_paths.embeddings` | string or null | Path to embedding npz |

---

## 3. CONCRETE INSTANCES

### 3.1 XRV DenseNet121 (from EXP-0012B)

```json
{{
  "model_id": "densenet121-res224-all",
  "model_family": "supervised_classifier",
  "framework": "torchxrayvision",
  "checkpoint_source": "TorchXRayVision v1.4.0",
  "source_experiment": "EXP-0012B",
  "input_manifest": "EXP-0012B/artifacts/sample_manifest.csv",
  "num_images": 100,
  "input_modality": "chest_xray",
  "preprocessing_contract": {{
    "target_size": [224, 224],
    "note": "Resized and normalized per TorchXRayVision defaults"
  }},
  "output_type": "logits",
  "output_shape": [100, 18],
  "output_dtype": "float32",
  "embedding_dim": null,
  "label_space": {{
    "type": "explicit",
    "count": 18,
    "labels": [{quoted_labels}],
    "mapped_to_target": 11,
    "mapped_labels": ["Atelectasis", "Consolidation", "Pneumothorax", "Edema", "Pleural Effusion", "Pneumonia", "Cardiomegaly", "Lung Lesion", "Fracture", "Lung Opacity", "Enlarged Cardiomediastinum"],
    "unmapped_labels": [{quoted_unmapped}]
  }},
  "requires_downstream_head": false,
  "downstream_head_description": null,
  "can_compute_direct_metrics": true,
  "supported_metrics": ["auroc"],
  "metric_prerequisites": null,
  "clinical_claims_allowed": false,
  "medical_evaluation_readiness": "sanity_only",
  "known_limitations": [
    "N=100 sample, high variance",
    "Deterministic random sampling (seed=42), not stratified",
    "2 of 11 mapped labels excluded due to single-class sample",
    "AUROC is pipeline sanity only, not clinical performance",
    "Label noise and class imbalance present in CheXpert validation set",
    "No external validation",
    "CPU-only inference"
  ],
  "artifact_paths": {{
    "manifest": "EXP-0012B/artifacts/sample_manifest.csv",
    "outputs": "EXP-0012B/artifacts/xrv_chexpert_outputs.csv",
    "metrics": "EXP-0012B/artifacts/metric_sanity.json",
    "embeddings": null
  }}
}}
```

### 3.2 RAD-DINO (from EXP-0013)

```json
{{
  "model_id": "microsoft/rad-dino",
  "model_family": "foundation_encoder",
  "framework": "transformers (HuggingFace)",
  "checkpoint_source": "local_cache (downloaded during EXP-0013)",
  "source_experiment": "EXP-0013",
  "input_manifest": "EXP-0013/artifacts/* (same sample as EXP-0012B)",
  "num_images": 100,
  "input_modality": "chest_xray",
  "preprocessing_contract": {{
    "target_size": [224, 224],
    "note": "Resized and normalized per RAD-DINO default processor"
  }},
  "output_type": "embeddings",
  "output_shape": [100, 768],
  "output_dtype": "float32",
  "embedding_dim": 768,
  "label_space": null,
  "requires_downstream_head": true,
  "downstream_head_description": "Linear probe, MLP, or specialized classifier head trained on labeled data",
  "can_compute_direct_metrics": false,
  "supported_metrics": [],
  "metric_prerequisites": ["Train downstream classification head on labeled data"],
  "clinical_claims_allowed": false,
  "medical_evaluation_readiness": "not_ready",
  "known_limitations": [
    "Embeddings only — no disease semantics without downstream training",
    "CPU-only inference in EXP-0013",
    "Embedding quality not evaluated",
    "Public checkpoint may not match paper setup (EXP-0003 finding)",
    "No downstream classification performed",
    "No AUROC or clinical metric computable without head",
    "No external validation"
  ],
  "artifact_paths": {{
    "manifest": "EXP-0012B/artifacts/sample_manifest.csv",
    "outputs": "EXP-0013/artifacts/rad_dino_embedding_summary.json",
    "metrics": null,
    "embeddings": "EXP-0013/artifacts/rad_dino_embeddings.npz"
  }}
}}
```

---

## 4. Contract Enforcement Rules

1. **Output type drives metric selection.** Classifier outputs (`logits`, `probabilities`) can use direct label metrics. Embedding outputs require a downstream head before metric computation.

2. **Label space null means non-classifier.** If `label_space` is `null`, the model is not a direct classifier. AUROC, F1, and other label-based metrics cannot be computed directly.

3. **`requires_downstream_head` and `can_compute_direct_metrics` must be consistent.** If one is `true`, the other must be `false`, and vice versa.

4. **`clinical_claims_allowed` is always `false` at experiment level.** It can only change to `true` after external clinical validation with human approval.

5. **Artifact paths must point to readable files.** The runner or tooling must verify path existence before using the contract.

6. **Input manifest must be shared or verified aligned** when comparing models on the same sample.

---

## 5. Multi-Model Contract Comparison Summary

| Dimension | XRV DenseNet121 | RAD-DINO |
|-----------|----------------|----------|
| Model family | Supervised classifier | Foundation encoder |
| Output type | Pathology logits | Image embeddings |
| Output shape | [N, 18] | [N, 768] |
| Label space | 18 explicit XRV pathologies | None |
| CheXpert mapping | Partial (11/18) | None |
| Direct metrics | Yes (AUROC per label) | No |
| Needs downstream head | No | Yes |
| Clinical readiness | Sanity only | Not ready |

---

## 6. Limitations

This draft is based on a read-only comparison of two prior experiments on a small deterministic random sample (N=100, seed=42).

- No new inference was run.
- No RAD-DINO classification was performed.
- No AUROC was computed for RAD-DINO.
- The adapter contract has not been validated with additional model families.
- Clinical claims are not permitted based on this analysis.

---
*End of CeXaR Model Adapter Contract Draft*
"""
with open(os.path.join(ARTIFACTS_DIR, "cexar_adapter_contract_draft.md"), "w", encoding="utf-8") as f:
    f.write(adapter_md)

print("Phase 4 COMPLETE: CeXaR adapter contract draft written.")

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
print(f"All outputs written to {ARTIFACTS_DIR}")
print("  - sample_alignment_report.json")
print("  - model_output_contract_comparison.json")
print("  - cexar_adapter_contract_draft.md")