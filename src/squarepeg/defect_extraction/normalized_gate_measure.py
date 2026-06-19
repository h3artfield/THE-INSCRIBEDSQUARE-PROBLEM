"""Normalized gate measures (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Point = tuple[float, float]

MeasureType = Literal[
    "ATOMIC",
    "FINITELY_SUPPORTED",
    "BOUNDARY_ARC",
    "DIFFUSE",
    "SINGULAR_CONTINUOUS",
    "MULTICENTER",
]


@dataclass
class NormalizedGate:
    gate_id: str
    position: Point
    hull_index: int


@dataclass
class GateMeasure:
    weights: list[float]
    positions: list[Point]
    center: Point
    diameter: float


@dataclass
class GateMeasureLimit:
    measure_type: MeasureType
    nu_weights: list[float]
    nu_positions: list[Point]
    convergence: bool
    messages: list[str]


def normalize_hull(
    gates: list[NormalizedGate],
    *,
    center: Point | None = None,
    diameter_r: float = 1.0,
) -> GateMeasure:
    """H_tilde = (H - z_n)/r_n; gates normalized to unit hull."""
    if not gates:
        return GateMeasure([], [], (0.0, 0.0), diameter_r)
    cx = sum(g.position[0] for g in gates) / len(gates)
    cy = sum(g.position[1] for g in gates) / len(gates)
    z = center or (cx, cy)
    r = max(diameter_r, 1e-9)
    positions = [((g.position[0] - z[0]) / r, (g.position[1] - z[1]) / r) for g in gates]
    w = 1.0 / len(gates)
    return GateMeasure(weights=[w] * len(gates), positions=positions, center=(0.0, 0.0), diameter=1.0)


def gate_spacing_normalized(gates: list[Point], r: float) -> list[float]:
    """ell_{n,i} = |g_{i+1}-g_i|/r_n cyclically."""
    if len(gates) < 2 or r <= 0:
        return []
    spacings: list[float] = []
    n = len(gates)
    for i in range(n):
        dx = gates[(i + 1) % n][0] - gates[i][0]
        dy = gates[(i + 1) % n][1] - gates[i][1]
        spacings.append(min(1.0, (dx * dx + dy * dy) ** 0.5 / r))
    return spacings


def extract_measure_limit(
    sequence: list[GateMeasure],
) -> GateMeasureLimit:
    """nu_n => nu by compactness on probability measures on unit hull."""
    if not sequence:
        return GateMeasureLimit("ATOMIC", [], [], False, ["Empty sequence"])
    last = sequence[-1]
    n = len(last.weights)
    if n <= 4:
        mtype: MeasureType = "ATOMIC"
    elif n <= 20:
        mtype = "FINITELY_SUPPORTED"
    else:
        max_w = max(last.weights) if last.weights else 0
        mtype = "DIFFUSE" if max_w < 0.1 else "BOUNDARY_ARC"
    centers = _detect_centers(last.positions)
    if len(centers) >= 2:
        mtype = "MULTICENTER"
    return GateMeasureLimit(
        measure_type=mtype,
        nu_weights=last.weights,
        nu_positions=last.positions,
        convergence=len(sequence) >= 2,
        messages=[f"Limit type: {mtype}, n={n}"],
    )


def _detect_centers(positions: list[Point], threshold: float = 0.3) -> list[Point]:
    if not positions:
        return []
    clusters: list[list[Point]] = [[positions[0]]]
    for p in positions[1:]:
        placed = False
        for cl in clusters:
            cx = sum(x[0] for x in cl) / len(cl)
            cy = sum(x[1] for x in cl) / len(cl)
            if ((p[0] - cx) ** 2 + (p[1] - cy) ** 2) ** 0.5 < threshold:
                cl.append(p)
                placed = True
                break
        if not placed:
            clusters.append([p])
    return [(sum(p[0] for p in cl) / len(cl), sum(p[1] for p in cl) / len(cl)) for cl in clusters]
