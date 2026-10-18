"""Training load helpers for JuniorCoach.

Pure-stdlib utilities for tracking session load (RPE x minutes) and the
acute:chronic workload ratio (ACWR) used to flag sudden load spikes.
No network access, no I/O, nothing that serves.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence

__all__ = [
    "session_load",
    "rolling_mean",
    "acwr",
    "acwr_zone",
]


def session_load(rpe: float, minutes: float) -> float:
    """Return session RPE load (rpe * minutes).

    >>> session_load(6, 45)
    270.0
    """
    if not 0 <= rpe <= 10:
        raise ValueError("rpe must be between 0 and 10")
    if minutes < 0:
        raise ValueError("minutes must be non-negative")
    return float(rpe) * float(minutes)


def rolling_mean(values: Sequence[float], window: int) -> float:
    """Mean of the last ``window`` values (fewer if not enough history).

    >>> rolling_mean([1, 2, 3, 4], 2)
    3.5
    >>> rolling_mean([], 7)
    0.0
    """
    if window <= 0:
        raise ValueError("window must be positive")
    tail = list(values)[-window:]
    if not tail:
        return 0.0
    return sum(tail) / len(tail)


def acwr(daily_loads: Iterable[float], acute: int = 7, chronic: int = 28) -> float:
    """Acute:chronic workload ratio from daily loads (oldest first).

    Returns 0.0 when chronic load is zero.

    >>> acwr([100] * 28)
    1.0
    >>> round(acwr([100] * 21 + [200] * 7), 3)
    1.6
    """
    if acute <= 0 or chronic <= 0 or acute > chronic:
        raise ValueError("need 0 < acute <= chronic")
    loads: List[float] = [float(x) for x in daily_loads]
    chronic_mean = rolling_mean(loads, chronic)
    if chronic_mean == 0:
        return 0.0
    return rolling_mean(loads, acute) / chronic_mean


def acwr_zone(ratio: float) -> str:
    """Classify an ACWR value.

    >>> [acwr_zone(r) for r in (0.5, 1.0, 1.4, 1.8)]
    ['under', 'sweet', 'caution', 'danger']
    """
    if ratio < 0.8:
        return "under"
    if ratio <= 1.3:
        return "sweet"
    if ratio <= 1.5:
        return "caution"
    return "danger"


if __name__ == "__main__":
    import doctest

    failures, _ = doctest.testmod()
    raise SystemExit(1 if failures else 0)
