"""Sweat-rate and fluid-replacement helpers for JuniorCoach.

Pure functions, standard library only. Sweat rate follows the common
field method: (pre-weight - post-weight + fluid intake - urine) / hours.
"""
from __future__ import annotations

__all__ = ["sweat_rate_l_per_h", "percent_body_mass_loss", "replacement_volume_l", "hydration_flag"]


def sweat_rate_l_per_h(pre_kg: float, post_kg: float, intake_l: float,
                       duration_h: float, urine_l: float = 0.0) -> float:
    """Litres of sweat lost per hour (1 kg of mass ~ 1 L of fluid)."""
    if duration_h <= 0:
        raise ValueError("duration_h must be positive")
    if pre_kg <= 0 or post_kg <= 0:
        raise ValueError("weights must be positive")
    if intake_l < 0 or urine_l < 0:
        raise ValueError("fluid volumes cannot be negative")
    loss = (pre_kg - post_kg) + intake_l - urine_l
    return max(loss, 0.0) / duration_h


def percent_body_mass_loss(pre_kg: float, post_kg: float) -> float:
    """Percent of pre-session body mass lost (negative means gained)."""
    if pre_kg <= 0:
        raise ValueError("pre_kg must be positive")
    return (pre_kg - post_kg) / pre_kg * 100.0


def replacement_volume_l(pre_kg: float, post_kg: float, factor: float = 1.5) -> float:
    """Fluid to drink after a session: net mass lost times factor (default 150%)."""
    if factor <= 0:
        raise ValueError("factor must be positive")
    return max(pre_kg - post_kg, 0.0) * factor


def hydration_flag(pct_loss: float) -> str:
    """Coach-facing label for percent body-mass loss."""
    if pct_loss < 0:
        return "overdrinking"
    if pct_loss < 1.0:
        return "ok"
    if pct_loss < 2.0:
        return "mild"
    return "high"


if __name__ == "__main__":
    assert abs(sweat_rate_l_per_h(60.0, 59.0, 0.5, 1.5) - 1.0) < 1e-9
    assert sweat_rate_l_per_h(60.0, 60.5, 0.0, 1.0) == 0.0
    assert abs(percent_body_mass_loss(50.0, 49.0) - 2.0) < 1e-9
    assert abs(replacement_volume_l(50.0, 49.2) - 1.2) < 1e-9
    assert [hydration_flag(x) for x in (-0.5, 0.5, 1.5, 2.5)] == ["overdrinking", "ok", "mild", "high"]
    for bad in ((60, 59, 0.5, 0), (0, 59, 0.5, 1), (60, 59, -1, 1)):
        try:
            sweat_rate_l_per_h(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(bad)
    print("sweat_rate self-check ok")
