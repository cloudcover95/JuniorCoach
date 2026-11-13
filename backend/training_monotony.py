"""Foster training monotony and strain from daily training load.

monotony = mean(load) / stdev(load) over a window (default 7 days)
strain   = weekly_total_load * monotony
Pure stdlib, additive utility.
"""
from __future__ import annotations

from math import sqrt
from typing import Sequence


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def _pstdev(xs: Sequence[float]) -> float:
    m = _mean(xs)
    return sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def monotony(daily_loads: Sequence[float]) -> float:
    """Mean over population stdev; inf if loads are identical and nonzero, 0 if all zero."""
    if not daily_loads:
        raise ValueError("daily_loads must not be empty")
    if any(x < 0 for x in daily_loads):
        raise ValueError("loads must be non-negative")
    sd = _pstdev(daily_loads)
    m = _mean(daily_loads)
    if sd == 0:
        return 0.0 if m == 0 else float("inf")
    return m / sd


def strain(daily_loads: Sequence[float]) -> float:
    """Total load times monotony."""
    mono = monotony(daily_loads)
    total = sum(daily_loads)
    if total == 0:
        return 0.0
    return total * mono


def rolling_monotony(daily_loads: Sequence[float], window: int = 7) -> list[float]:
    if window < 2:
        raise ValueError("window must be >= 2")
    return [monotony(daily_loads[i - window:i]) for i in range(window, len(daily_loads) + 1)]


def _self_check() -> None:
    assert monotony([0] * 7) == 0.0
    assert monotony([5] * 7) == float("inf")
    m = monotony([100, 200, 100, 200, 100, 200, 100])
    assert 2.0 < m < 4.0, m
    assert abs(strain([1, 2, 3]) - 6 * (2 / sqrt(2 / 3))) < 1e-9
    assert len(rolling_monotony(list(range(1, 11)), 7)) == 4
    try:
        monotony([])
    except ValueError:
        pass
    else:
        raise AssertionError


if __name__ == "__main__":
    _self_check()
    print("ok")
