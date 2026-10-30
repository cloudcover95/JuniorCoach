"""Heart-rate training zones (Karvonen / heart-rate-reserve method).

Pure-Python, no dependencies, no network, no server.
Run directly to execute the built-in self-check.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

# Zone name -> (low, high) fraction of heart-rate reserve.
ZONES: List[Tuple[str, float, float]] = [
    ("Z1 recovery", 0.50, 0.60),
    ("Z2 endurance", 0.60, 0.70),
    ("Z3 tempo", 0.70, 0.80),
    ("Z4 threshold", 0.80, 0.90),
    ("Z5 max", 0.90, 1.00),
]


def estimate_max_hr(age: float) -> float:
    """Tanaka estimate: 208 - 0.7 * age."""
    if age <= 0:
        raise ValueError("age must be positive")
    return 208.0 - 0.7 * age


def karvonen(max_hr: float, rest_hr: float, intensity: float) -> float:
    """Target HR = rest + intensity * (max - rest)."""
    if not 0.0 <= intensity <= 1.0:
        raise ValueError("intensity must be within [0, 1]")
    if rest_hr <= 0 or max_hr <= rest_hr:
        raise ValueError("need 0 < rest_hr < max_hr")
    return rest_hr + intensity * (max_hr - rest_hr)


def zone_table(max_hr: float, rest_hr: float) -> Dict[str, Tuple[int, int]]:
    """Return rounded bpm bounds for each zone."""
    return {
        name: (round(karvonen(max_hr, rest_hr, lo)), round(karvonen(max_hr, rest_hr, hi)))
        for name, lo, hi in ZONES
    }


def zone_for(hr: float, max_hr: float, rest_hr: float) -> str:
    """Name of the zone containing hr ('below Z1' if under 50% HRR)."""
    frac = (hr - rest_hr) / (max_hr - rest_hr)
    if frac < ZONES[0][1]:
        return "below Z1"
    for name, lo, hi in ZONES:
        if lo <= frac < hi:
            return name
    return ZONES[-1][0]


def _self_check() -> None:
    assert abs(estimate_max_hr(20) - 194.0) < 1e-9
    assert karvonen(200, 60, 0.0) == 60
    assert karvonen(200, 60, 1.0) == 200
    assert abs(karvonen(200, 60, 0.5) - 130.0) < 1e-9
    table = zone_table(200, 60)
    assert table["Z1 recovery"] == (130, 144)
    assert table["Z5 max"] == (186, 200)
    bounds = [b for name, _, _ in ZONES for b in table[name]]
    assert bounds == sorted(bounds)
    assert zone_for(100, 200, 60) == "below Z1"
    assert zone_for(150, 200, 60) == "Z2 endurance"
    assert zone_for(200, 200, 60) == "Z5 max"
    for bad in ((-0.1,), (1.1,)):
        try:
            karvonen(200, 60, bad[0])
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    print("hr_zones self-check OK")


if __name__ == "__main__":
    _self_check()
