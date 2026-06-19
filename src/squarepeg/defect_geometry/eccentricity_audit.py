"""Eccentricity audit: exclude Directive 020 thin-ellipse counterexamples."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_geometry.annular_graph import AnnularGraphConstants, radial_layer_from_ellipse


@dataclass
class EllipseEccentricityAudit:
    semi_major: float
    semi_minor: float
    K_ratio: float
    in_annular_graph_for_K: bool
    fixed_K_excluded: bool


def ellipse_eccentricity_K(a: float, b: float) -> float:
    """K = max r / min r = a/b for axis-aligned ellipse radial graph."""
    if b <= 0:
        return float("inf")
    return a / b


def audit_thin_ellipse(a: float, b: float, K_max: float = 2.0) -> EllipseEccentricityAudit:
    K = ellipse_eccentricity_K(a, b)
    layer = radial_layer_from_ellipse(a, b)
    K_sampled = layer.eccentricity_K()
    return EllipseEccentricityAudit(
        semi_major=a,
        semi_minor=b,
        K_ratio=K_sampled,
        in_annular_graph_for_K=K_sampled <= K_max,
        fixed_K_excluded=K_sampled > K_max,
    )


def directive_020_falsification_excluded(K_bound: float = 2.0) -> bool:
    """
    Thin ellipses a >> b have K = a/b -> infinity, hence leave every fixed-K class.
    """
    audits = [audit_thin_ellipse(a, 0.1 * a, K_bound) for a in [2.0, 5.0, 10.0]]
    return all(a.fixed_K_excluded for a in audits)


def thin_ellipse_K_diverges() -> str:
    return "For a_j/b_j -> infinity, K_j = a_j/b_j -> infinity, excluding all fixed-K ANNULAR_GRAPH classes."


@dataclass
class CounterexampleAttempt:
    name: str
    passes_annular_graph: bool
    breaks_reference_closeness: bool
    failure_mode: str


def search_annular_counterexamples(K_bound: float = 2.0) -> list[CounterexampleAttempt]:
    """Directive 021 Part 6: attempted falsifications of annular-graph sufficiency."""
    from squarepeg.defect_geometry.annular_graph import (
        AnnularGraphConstants,
        AnnularGraphPacket,
        RadialLayer,
        radial_layer_from_ellipse,
        validate_annular_graph,
    )
    from squarepeg.defect_geometry.radial_correspondence import build_radial_correspondence, normalize_layer_pair
    from squarepeg.defect_geometry.reference_cyclic_certificate import rho_cyc_reference

    rho = rho_cyc_reference()
    c = AnnularGraphConstants(K=K_bound, L=0.5, g_minus=0.35, g_plus=0.65, w_corr=0.12, zeta=0.08)
    attempts: list[CounterexampleAttempt] = []

    def _record(name: str, pkt: AnnularGraphPacket) -> None:
        ok = validate_annular_graph(pkt)
        pair = normalize_layer_pair(pkt.layers[0], pkt.layers[1])
        corr = build_radial_correspondence(pair)
        breaks = ok and corr.max_distance >= rho
        mode = "excluded_by_annular_graph" if not ok else (
            "defeats_closeness" if breaks else "no_counterexample"
        )
        attempts.append(
            CounterexampleAttempt(
                name=name,
                passes_annular_graph=ok,
                breaks_reference_closeness=breaks,
                failure_mode=mode,
            )
        )

    # Thin ellipse: fails K bound
    _record(
        "thin_eccentric_ellipse",
        AnnularGraphPacket(
            layers=[radial_layer_from_ellipse(10.0, 0.5), radial_layer_from_ellipse(4.0, 0.2)],
            corridor_width=0.02,
            constants=c,
        ),
    )

    # Off-center circles: fails center drift for tight regime
    outer = radial_layer_from_ellipse(1.0, 1.0)
    inner = radial_layer_from_ellipse(0.45, 0.45)
    inner_off = RadialLayer(
        center=(0.15, 0.0),
        radii=inner.radii,
        n_theta=inner.n_theta,
        diameter=inner.diameter,
        winding_sign=1,
    )
    _record(
        "off_center_circles",
        AnnularGraphPacket(layers=[outer, inner_off], corridor_width=0.02, constants=c),
    )

    # High-frequency ripple on outer (fails angular L for small L)
    import math

    n = 64
    radii_ripple = []
    for i in range(n):
        t = 2 * math.pi * i / n
        radii_ripple.append(1.0 + 0.08 * math.sin(8 * t))
    ripple = RadialLayer(center=(0.0, 0.0), radii=radii_ripple, n_theta=n, diameter=2.0, winding_sign=1)
    _record(
        "angular_ripple",
        AnnularGraphPacket(
            layers=[ripple, radial_layer_from_ellipse(0.45, 0.45)],
            corridor_width=0.02,
            constants=AnnularGraphConstants(K=1.2, L=0.02, g_minus=0.35, g_plus=0.65, w_corr=0.05, zeta=0.02),
        ),
    )

    # Rapid center drift across layers
    inner_drift = RadialLayer(center=(0.12, 0.0), radii=inner.radii, n_theta=n, diameter=0.9, winding_sign=1)
    _record(
        "rapid_center_drift",
        AnnularGraphPacket(
            layers=[outer, inner_drift],
            corridor_width=0.02,
            constants=AnnularGraphConstants(K=1.05, L=0.05, g_minus=0.35, g_plus=0.65, w_corr=0.05, zeta=0.05),
        ),
    )

    return attempts


def no_successful_counterexample() -> bool:
    """True when every search attempt is excluded or does not break closeness."""
    attempts = search_annular_counterexamples()
    return not any(a.passes_annular_graph and a.breaks_reference_closeness for a in attempts)
