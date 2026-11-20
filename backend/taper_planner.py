"""Exponential taper planner: reduce training volume over N days before an event.

Pure stdlib, additive module. No I/O, no network.
"""
from __future__ import annotations

import math
from typing import List


def taper_plan(base_load: float, days: int, reduction: float = 0.4, tau_frac: float = 0.5) -> List[float]:
    """Return daily loads that decay exponentially from base_load.

    reduction: total fractional drop reached on the final day (0..1).
    tau_frac: shape; smaller values front-load the drop.
    """
    if base_load < 0:
        raise ValueError("base_load must be >= 0")
    if days < 1:
        raise ValueError("days must be >= 1")
    if not 0.0 <= reduction < 1.0:
        raise ValueError("reduction must be in [0, 1)")
    if tau_frac <= 0:
        raise ValueError("tau_frac must be > 0")
    if days == 1:
        return [base_load * (1.0 - reduction)]
    tau = tau_frac * days
    end = 1.0 - math.exp(-(days - 1) / tau)
    out = []
    for d in range(days):
        shape = (1.0 - math.exp(-d / tau)) / end if end else 0.0
        out.append(base_load * (1.0 - reduction * shape))
    return out


def _self_check() -> None:
    p = taper_plan(100.0, 7, 0.4)
    assert len(p) == 7
    assert abs(p[0] - 100.0) < 1e-9
    assert abs(p[-1] - 60.0) < 1e-9
    assert all(a >= b for a, b in zip(p, p[1:]))
    assert taper_plan(50.0, 1, 0.2) == [40.0]
    try:
        taper_plan(1, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


if __name__ == "__main__":
    _self_check()
    print("taper_planner self-check ok")
