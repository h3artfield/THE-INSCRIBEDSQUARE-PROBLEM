"""Center coherence for annular packet forests (Directive 026)."""

from __future__ import annotations

from dataclasses import dataclass
import math

from squarepeg.defect_surgery.annular_attachment_order import GatePair


@dataclass
class CenterCoherenceAudit:
    common_center: bool
    max_drift_ratio: float
    passes: bool


def center_drift(g1: GatePair, g2: GatePair) -> float:
    return math.hypot(g1.center[0] - g2.center[0], g1.center[1] - g2.center[1])


def audit_center_coherence(
    gates: list[GatePair],
    *,
    c_center: float = 1.5,
) -> CenterCoherenceAudit:
    """
    Common center OR controlled drift |c_{i+1}-c_i| <= C_center min(r_i,r_{i+1}).
    """
    if not gates:
        return CenterCoherenceAudit(True, 0.0, True)
    c0 = gates[0].center
    common = all(math.hypot(g.center[0] - c0[0], g.center[1] - c0[1]) < 1e-6 for g in gates)
    max_ratio = 0.0
    ordered = sorted(gates, key=lambda g: g.lo)
    for i in range(len(ordered) - 1):
        g1, g2 = ordered[i], ordered[i + 1]
        d = center_drift(g1, g2)
        rmin = min(g1.radius, g2.radius)
        if rmin > 1e-12:
            max_ratio = max(max_ratio, d / rmin)
    ok = common or max_ratio <= c_center
    return CenterCoherenceAudit(common_center=common, max_drift_ratio=max_ratio, passes=ok)
