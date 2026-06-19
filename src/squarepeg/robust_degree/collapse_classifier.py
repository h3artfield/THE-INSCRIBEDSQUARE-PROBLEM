"""Degree-collapse classification and counterexample search diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from squarepeg.robust_degree.area_defect import alpha_P_delta, alpha_sequence_limsup
from squarepeg.robust_degree.polygon_extractor import rho_square_certified_lower_bound_polygon
from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full

SearchInterpretation = Literal[
    "no_protected_square",
    "certificate_not_found",
    "all_families",
    "interval_failure",
    "unsupported_rank",
    "positive_robust_degree",
    "collapse_observed",
    "area_tight_subsequence",
    "forbidden_pattern_suspected",
]


class CollapseMode(str, Enum):
    SIDE_TO_ZERO = "side_length_to_zero"
    PARAM_COLLISION = "parameter_collision"
    JACOBIAN_SINGULAR = "jacobian_singular"
    FAMILY_MERGE = "isolated_to_family"
    BOUNDARY_CROSS = "zero_crosses_boundary"
    WINDOW_DRIFT = "support_window_drift"
    UNKNOWN = "unknown"


@dataclass
class CollapseRecord:
    n: int
    rho_cert: float
    alpha_delta: float
    interpretation: SearchInterpretation
    collapse_modes: list[CollapseMode] = field(default_factory=list)


@dataclass
class SequenceDiagnostic:
    name: str
    records: list[CollapseRecord] = field(default_factory=list)
    rho_limsup: float = 0.0
    area_tight: bool | None = None
    forbidden_pattern: bool = False
    notes: list[str] = field(default_factory=list)


def classify_polygon_collapse(
    rho: float,
    breakdown: dict,
    side_lb: float = 0.0,
) -> list[CollapseMode]:
    modes: list[CollapseMode] = []
    if side_lb < 1e-6:
        modes.append(CollapseMode.SIDE_TO_ZERO)
    if breakdown.get("failed", 0) > 0 and breakdown.get("converted", 0) == 0:
        if breakdown.get("families", 0) > 0:
            modes.append(CollapseMode.FAMILY_MERGE)
        if breakdown.get("unsupported", 0) > 0:
            modes.append(CollapseMode.UNKNOWN)
    if rho <= 0 and breakdown.get("isolated", 0) > 0:
        modes.append(CollapseMode.JACOBIAN_SINGULAR)
    if not modes:
        modes.append(CollapseMode.UNKNOWN)
    return modes


def diagnose_polygon_sequence(
    name: str,
    polygons: list[PolygonCurve],
    deltas: list[float],
) -> SequenceDiagnostic:
    diag = SequenceDiagnostic(name=name)
    rhos: list[float] = []
    for n_idx, poly in enumerate(polygons):
        result = solve_polygon_full(poly)
        rho, breakdown = rho_square_certified_lower_bound_polygon(poly, result)
        rhos.append(rho)
        g = _poly_to_gamma(poly)
        alpha = alpha_P_delta(g, deltas[min(n_idx, len(deltas) - 1)])
        interp: SearchInterpretation
        if rho > 0:
            interp = "positive_robust_degree"
        elif breakdown.get("isolated", 0) == 0:
            interp = "certificate_not_found" if result.families_1d else "no_protected_square"
        elif breakdown.get("families", 0) > 0:
            interp = "all_families"
        else:
            interp = "collapse_observed"
        modes = classify_polygon_collapse(rho, breakdown)
        diag.records.append(CollapseRecord(n_idx, rho, alpha, interp, modes))
    diag.rho_limsup = max(rhos) if rhos else 0.0
    gammas = [_poly_to_gamma(p) for p in polygons]
    diag.area_tight = all(
        alpha_sequence_limsup(gammas, d) < 0.05 for d in deltas[-2:]
    )
    if diag.rho_limsup < 1e-6 and diag.area_tight is False:
        diag.forbidden_pattern = True
        diag.notes.append("rho->0 without apparent area-tightness (diagnostic only)")
    return diag


def _poly_to_gamma(poly: PolygonCurve):
    from squarepeg.robust_degree.area_defect import polygon_gamma

    verts = [(float(v[0]), float(v[1])) for v in poly.vertices]
    return polygon_gamma(verts)


def run_counterexample_search() -> list[SequenceDiagnostic]:
    """Diagnostic search over built-in curve families (not proof)."""
    from squarepeg.residual_curves.canonical import CanonicalDoubleSpiral

    ds = CanonicalDoubleSpiral()
    deltas = [0.5, 0.25, 0.1, 0.05]
    diags: list[SequenceDiagnostic] = []
    for turns in (3, 4, 5):
        verts = ds.truncated_polygon(turns)
        from squarepeg.curves.polygon import PolygonCurve

        poly = PolygonCurve(verts)
        diags.append(diagnose_polygon_sequence(f"double_spiral_N{turns}", [poly], deltas))
    return diags
