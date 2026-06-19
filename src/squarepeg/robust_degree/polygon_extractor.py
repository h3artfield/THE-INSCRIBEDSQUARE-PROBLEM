"""Convert exact polygon square certificates to protected degree boxes."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal

from squarepeg.certificates.schema import SquareCertificate
from squarepeg.curves.polygon import PolygonCurve
from squarepeg.robust_degree.degree_certificate import DegreeCertificate, from_protected_box
from squarepeg.robust_degree.perturbation_radius import rho_square_box
from squarepeg.robust_degree.protected_box import ProtectedSquareBox, is_protected_square_box

ConversionStatus = Literal[
    "converted",
    "rank_not_six",
    "singular_jacobian",
    "boundary_failed",
    "collision",
    "unsupported_family",
]


@dataclass
class ProtectedSquareCertificate:
    square_cert: SquareCertificate
    protected_box: ProtectedSquareBox
    degree_cert: DegreeCertificate | None
    conversion_status: ConversionStatus
    rho_certified_lower_bound: float = 0.0
    messages: list[str] = field(default_factory=list)


def _polygon_gamma(polygon: PolygonCurve, edges: tuple[int, int, int, int]):
    def gamma(theta: float) -> tuple[float, float]:
        i = min(3, max(0, int(theta)))
        t = theta - i
        p = polygon.evaluate_edge(edges[i], Fraction(t).limit_denominator(10**6))
        return float(p[0]), float(p[1])

    return gamma


def verify_rank_six(polygon: PolygonCurve, cert: SquareCertificate) -> bool:
    from squarepeg.exact_squares.validator import build_equations_independent
    from squarepeg.exact_squares.families import solve_affine_system

    matrix, rhs = build_equations_independent(polygon, cert.edge_indices, cert.orientation)
    sol = solve_affine_system(matrix, rhs)
    return sol.rank == 6


def convert_isolated_square(
    polygon: PolygonCurve,
    cert: SquareCertificate,
    *,
    param_radius: float = 0.05,
    boundary_margin: float | None = None,
) -> ProtectedSquareCertificate:
    if cert.certificate_type != "exact":
        return ProtectedSquareCertificate(
            cert,
            ProtectedSquareBox(windows=((0, 1), (1, 2), (2, 3), (3, 4))),
            None,
            "unsupported_family",
            messages=["not an isolated exact certificate"],
        )
    if not verify_rank_six(polygon, cert):
        return ProtectedSquareCertificate(
            cert,
            ProtectedSquareBox(windows=((0, 1), (1, 2), (2, 3), (3, 4))),
            None,
            "rank_not_six",
            messages=["linear system rank != 6"],
        )
    params = [float(Fraction(p)) for p in cert.edge_parameters]
    u_box = tuple(
        (max(0.0, p - param_radius), min(1.0, p + param_radius)) for p in params
    )
    windows = ((0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0))
    gamma = _polygon_gamma(polygon, cert.edge_indices)
    box = ProtectedSquareBox(windows=windows, u_box=u_box)
    checked = is_protected_square_box(gamma, box, boundary_margin=boundary_margin)
    if checked.interpretation != "protected":
        status: ConversionStatus = "boundary_failed"
        if checked.interpretation == "singular_jacobian":
            status = "singular_jacobian"
        elif checked.interpretation == "collision_risk":
            status = "collision"
        return ProtectedSquareCertificate(cert, checked, None, status, messages=checked.messages)
    deg = from_protected_box(checked)
    rho, _ = rho_square_box(gamma, checked, boundary_margin=checked.boundary_margin)
    return ProtectedSquareCertificate(
        cert, checked, deg, "converted", rho_certified_lower_bound=rho, messages=["rank-6 isolated converted"]
    )


def rho_square_certified_lower_bound_polygon(polygon: PolygonCurve, solve_result) -> tuple[float, dict]:
    """Computational lower bound underline_rho at fixed search level — NOT intrinsic rho."""
    breakdown = {
        "isolated": 0,
        "converted": 0,
        "failed": 0,
        "families": len(solve_result.families_1d),
        "unsupported": len(solve_result.unsupported),
    }
    best = 0.0
    for cert in solve_result.isolated:
        breakdown["isolated"] += 1
        conv = convert_isolated_square(polygon, cert)
        if conv.conversion_status == "converted":
            breakdown["converted"] += 1
            best = max(best, conv.rho_certified_lower_bound)
        else:
            breakdown["failed"] += 1
    return best, breakdown


# Deprecated alias
rho_square_cert_polygon = rho_square_certified_lower_bound_polygon
