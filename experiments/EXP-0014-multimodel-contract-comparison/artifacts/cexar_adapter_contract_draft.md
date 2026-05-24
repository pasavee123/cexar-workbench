# CeXaR Model Adapter Contract (Draft)

> Generated: 2026-05-24T02:20:01.680478+07:00
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
{
  "model_id": "densenet121-res224-all",
  "model_family": "supervised_classifier",
  "framework": "torchxrayvision",
  "checkpoint_source": "TorchXRayVision v1.4.0",
  "source_experiment": "EXP-0012B",
  "input_manifest": "EXP-0012B/artifacts/sample_manifest.csv",
  "num_images": 100,
  "input_modality": "chest_xray",
  "preprocessing_contract": {
    "target_size": [224, 224],
    "note": "Resized and normalized per TorchXRayVision defaults"
  },
  "output_type": "logits",
  "output_shape": [100, 18],
  "output_dtype": "float32",
  "embedding_dim": null,
  "label_space": {
    "type": "explicit",
    "count": 18,
    "labels": ["Atelectasis", "Consolidation", "Infiltration", "Pneumothorax", "Edema", "Emphysema", "Fibrosis", "Effusion", "Pneumonia", "Pleural_Thickening", "Cardiomegaly", "Nodule", "Mass", "Hernia", "Lung Lesion", "Fracture", "Lung Opacity", "Enlarged Cardiomediastinum"],
    "mapped_to_target": 11,
    "mapped_labels": ["Atelectasis", "Consolidation", "Pneumothorax", "Edema", "Pleural Effusion", "Pneumonia", "Cardiomegaly", "Lung Lesion", "Fracture", "Lung Opacity", "Enlarged Cardiomediastinum"],
    "unmapped_labels": ["Infiltration", "Emphysema", "Fibrosis", "Pleural_Thickening", "Nodule", "Mass", "Hernia"]
  },
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
  "artifact_paths": {
    "manifest": "EXP-0012B/artifacts/sample_manifest.csv",
    "outputs": "EXP-0012B/artifacts/xrv_chexpert_outputs.csv",
    "metrics": "EXP-0012B/artifacts/metric_sanity.json",
    "embeddings": null
  }
}
```

### 3.2 RAD-DINO (from EXP-0013)

```json
{
  "model_id": "microsoft/rad-dino",
  "model_family": "foundation_encoder",
  "framework": "transformers (HuggingFace)",
  "checkpoint_source": "local_cache (downloaded during EXP-0013)",
  "source_experiment": "EXP-0013",
  "input_manifest": "EXP-0013/artifacts/* (same sample as EXP-0012B)",
  "num_images": 100,
  "input_modality": "chest_xray",
  "preprocessing_contract": {
    "target_size": [224, 224],
    "note": "Resized and normalized per RAD-DINO default processor"
  },
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
  "artifact_paths": {
    "manifest": "EXP-0012B/artifacts/sample_manifest.csv",
    "outputs": "EXP-0013/artifacts/rad_dino_embedding_summary.json",
    "metrics": null,
    "embeddings": "EXP-0013/artifacts/rad_dino_embeddings.npz"
  }
}
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
