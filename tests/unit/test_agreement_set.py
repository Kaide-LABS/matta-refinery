"""Tests for ensemble agreement-set gating (renamed from conformal).

These pin the rename + the gating semantics: unanimous agreement
populates the set with coverage at agreement_target; total disagreement
defers via low_inter_model_agreement.
"""
from datetime import datetime

import pytest

from packages.schemas.defect_hypothesis import LikelyDefectClassHypothesis
from packages.uncertainty.agreement import (
    AgreementResult,
    CalibrationTable,
    compute_agreement_set,
)


def _calib(thresholds: dict[str, float]) -> CalibrationTable:
    return CalibrationTable(
        calibration_version="phase1-test",
        alpha=0.1,
        agreement_target=0.9,
        per_class_agreement_thresholds=thresholds,
        built_at=datetime(2026, 1, 1),
        holdout_size=30,
        seed=42,
    )


def _sample(classes: list[str]) -> LikelyDefectClassHypothesis:
    return LikelyDefectClassHypothesis(
        agreement_set=classes,  # type: ignore[arg-type]
        coverage=1.0,
        calibration_version="phase1-test",
        requires_human_review=False,
        rationale="test sample",
    )


def test_unanimous_agreement_populates_set():
    samples = [_sample(["porosity"]) for _ in range(3)]
    calib = _calib({"porosity": 0.1})
    result = compute_agreement_set(samples, calib)
    assert "porosity" in result.agreement_set
    assert result.coverage == calib.agreement_target
    assert result.requires_human_review is False
    assert result.deferral_reason is None
    assert result.inter_model_agreement_score == 1.0


def test_split_disagreement_defers():
    samples = [
        _sample(["porosity"]),
        _sample(["tool_wear"]),
        _sample(["surface_inclusions"]),
    ]
    calib = _calib({c: 0.1 for c in ["porosity", "tool_wear", "surface_inclusions"]})
    result = compute_agreement_set(samples, calib)
    assert result.agreement_set == []
    assert result.requires_human_review is True
    assert result.deferral_reason == "low_inter_model_agreement"
    # 1/3 vote share → ~0.33, below the 0.5 floor.
    assert result.inter_model_agreement_score < 0.5


def test_empty_ensemble_defers_insufficient():
    calib = _calib({"porosity": 0.1})
    result = compute_agreement_set([], calib)
    assert result.agreement_set == []
    assert result.deferral_reason == "insufficient_calibration_data"
    assert result.inter_model_agreement_score == 0.0


def test_majority_2_of_3_meets_threshold():
    samples = [_sample(["porosity"]), _sample(["porosity"]), _sample(["tool_wear"])]
    # threshold 0.4 → 1 - 0.4 = 0.6; vote share 2/3 ≈ 0.67 ≥ 0.6.
    calib = _calib({"porosity": 0.4, "tool_wear": 0.4})
    result = compute_agreement_set(samples, calib)
    assert "porosity" in result.agreement_set
    assert result.requires_human_review is False
