"""Session readiness score for JuniorCoach.

Combines sleep hours, resting-heart-rate delta from baseline, and a
1-5 wellness rating into a 0-100 readiness score and a coach label.
Pure stdlib, no network, nothing that serves.
"""
from __future__ import annotations

from typing import Tuple

__all__ = [
    "sleep_component",
    "rhr_component",
    "wellness_component",
    "readiness_score",
    "readiness_label",
]


def sleep_component(hours: float, target: float = 8.0) -> float:
    """0-100 points from sleep hours relative to a target (default 8h)."""
    if hours < 0:
        raise ValueError("hours must be non-negative")
    if target <= 0:
        raise ValueError("target must be positive")
    return max(0.0, min(100.0, (hours / target) * 100.0))


def rhr_component(resting_hr: float, baseline_hr: float) -> float:
    """0-100 points from resting HR vs baseline (lower than baseline scores higher).

    Each bpm above baseline costs 5 points; each bpm below adds 2.5, capped.
    """
    if resting_hr <= 0 or baseline_hr <= 0:
        raise ValueError("heart rates must be positive")
    delta = resting_hr - baseline_hr
    score = 100.0 - 5.0 * delta
    if delta < 0:
        score = 100.0 + 2.5 * (-delta)
    return max(0.0, min(100.0, score))


def wellness_component(rating: float) -> float:
    """Map a 1-5 wellness rating onto 0-100."""
    if not 1.0 <= rating <= 5.0:
        raise ValueError("rating must be between 1 and 5")
    return (rating - 1.0) / 4.0 * 100.0


def readiness_score(
    sleep_hours: float,
    resting_hr: float,
    baseline_hr: float,
    wellness: float,
    weights: Tuple[float, float, float] = (0.4, 0.35, 0.25),
) -> float:
    """Weighted readiness 0-100 from sleep, RHR, and wellness."""
    w_sleep, w_rhr, w_well = weights
    total_w = w_sleep + w_rhr + w_well
    if total_w <= 0:
        raise ValueError("weights must sum to a positive value")
    s = sleep_component(sleep_hours)
    r = rhr_component(resting_hr, baseline_hr)
    w = wellness_component(wellness)
    return (w_sleep * s + w_rhr * r + w_well * w) / total_w


def readiness_label(score: float) -> str:
    """Coach-facing label for a readiness score."""
    if score < 40:
        return "rest"
    if score < 60:
        return "easy"
    if score < 80:
        return "train"
    return "push"


def _self_check() -> None:
    assert abs(sleep_component(8.0) - 100.0) < 1e-9
    assert abs(sleep_component(4.0) - 50.0) < 1e-9
    assert abs(sleep_component(10.0) - 100.0) < 1e-9
    assert abs(rhr_component(50, 50) - 100.0) < 1e-9
    assert abs(rhr_component(55, 50) - 75.0) < 1e-9
    assert abs(rhr_component(46, 50) - 100.0) < 1e-9  # capped
    assert abs(wellness_component(1.0) - 0.0) < 1e-9
    assert abs(wellness_component(5.0) - 100.0) < 1e-9
    assert abs(wellness_component(3.0) - 50.0) < 1e-9
    # sleep 8 -> 100, rhr equal -> 100, wellness 5 -> 100 => 100
    assert abs(readiness_score(8.0, 50.0, 50.0, 5.0) - 100.0) < 1e-9
    # sleep 0 -> 0, rhr +20 -> 0, wellness 1 -> 0 => 0
    assert abs(readiness_score(0.0, 70.0, 50.0, 1.0) - 0.0) < 1e-9
    assert readiness_label(20) == "rest"
    assert readiness_label(50) == "easy"
    assert readiness_label(70) == "train"
    assert readiness_label(90) == "push"
    for bad in (
        lambda: sleep_component(-1),
        lambda: rhr_component(0, 50),
        lambda: wellness_component(0),
        lambda: wellness_component(6),
    ):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    print("readiness self-check OK")


if __name__ == "__main__":
    _self_check()
