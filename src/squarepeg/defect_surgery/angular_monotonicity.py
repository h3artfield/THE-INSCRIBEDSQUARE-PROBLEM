"""Angular monotonicity for annular attachment gates (Directive 026)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_surgery.annular_attachment_order import GatePair


@dataclass
class AngularMonotoneAudit:
    monotone_a: bool
    monotone_b: bool
    max_backtrack: float
    passes: bool


def _lifted_angle(p: tuple[float, float], center: tuple[float, float]) -> float:
    return math.atan2(p[1] - center[1], p[0] - center[0])


def angular_backtrack(angles: list[float]) -> float:
    """Max backward jump after unwrapping angles."""
    if len(angles) < 2:
        return 0.0
    unwrapped = [angles[0]]
    for a in angles[1:]:
        prev = unwrapped[-1]
        da = a - prev
        while da < -math.pi:
            da += 2 * math.pi
        while da > math.pi:
            da -= 2 * math.pi
        unwrapped.append(prev + da)
    back = 0.0
    for i in range(1, len(unwrapped)):
        if unwrapped[i] < unwrapped[i - 1]:
            back = max(back, unwrapped[i - 1] - unwrapped[i])
    return back


def audit_angular_monotone(
    gates: list[GatePair],
    *,
    eps_ang: float = 0.05,
) -> AngularMonotoneAudit:
    """ANGULAR_MONOTONE_ATTACHMENTS with bounded backtrack eps_ang."""
    if not gates:
        return AngularMonotoneAudit(True, True, 0.0, True)
    c = gates[0].center
    ang_a = [_lifted_angle(g.point_a, c) for g in sorted(gates, key=lambda g: g.lo)]
    ang_b = [_lifted_angle(g.point_b, c) for g in sorted(gates, key=lambda g: g.lo)]
    ba = angular_backtrack(ang_a)
    bb = angular_backtrack(ang_b)
    mono_a = ba <= eps_ang
    mono_b = bb <= eps_ang
    return AngularMonotoneAudit(
        monotone_a=mono_a,
        monotone_b=mono_b,
        max_backtrack=max(ba, bb),
        passes=mono_a and mono_b,
    )
