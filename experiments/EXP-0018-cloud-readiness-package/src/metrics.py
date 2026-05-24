"""Metric skeletons for research pipeline reporting."""

from __future__ import annotations


METRIC_NOTICE = "RESEARCH PIPELINE METRIC ONLY - NOT CLINICAL PERFORMANCE"


def compute_binary_metrics(*args, **kwargs):
    """TODO: Compute AUROC/AUPRC only when both classes are present."""
    raise NotImplementedError("Implemented in EXP-0019/EXP-0020.")


def should_mask_metric(positive_count: int, negative_count: int, min_count: int = 3) -> bool:
    return positive_count < min_count or negative_count < min_count

