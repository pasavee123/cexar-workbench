"""Patient-level split strategy skeletons for cloud experiments."""

from __future__ import annotations


def build_patient_level_split(*args, **kwargs):
    """TODO: Implement deterministic patient-level split with label constraints."""
    raise NotImplementedError("Implemented in EXP-0019/EXP-0020.")


def validate_split_class_counts(*args, **kwargs):
    """TODO: Validate per-label positive/negative counts per split."""
    raise NotImplementedError("Implemented in EXP-0019/EXP-0020.")

