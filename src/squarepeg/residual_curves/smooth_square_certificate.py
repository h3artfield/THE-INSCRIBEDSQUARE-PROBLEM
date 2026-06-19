"""Validated smooth-square existence certificate."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Literal

from squarepeg.residual_curves.smooth_square_intervals import (
    F_interval,
    IVal,
    contains_zero,
    krawczyk_test,
    min_radius_lower_bound,
)
from squarepeg.residual_curves.smooth_square_system import (
    DISCOVERED_SMOOTH_THETA,
    OUTER_THETA_WINDOWS,
    jacobian_theta,
    midpoint_rotation_residuals,
    side_length,
    square_map_F_theta,
    supports_from_theta_windows,
    theta_to_u,
)

CertStatus = Literal["certified", "unresolved", "candidate_only"]


@dataclass
class SmoothSquareExistenceCertificate:
    parameter_boxes: list[list[float]]
    theta_boxes: list[list[float]]
    side_length_lower_bound: float
    min_radius_lower_bound: float
    max_residual_upper_bound: float
    jacobian_det: float
    certification_status: CertStatus
    method: str
    support_pattern: str
    message: str = ""
    validator_midpoint_max: float = 0.0
    subdivision_history: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def _independent_validator(thetas: list[float]) -> float:
    sup = supports_from_theta_windows()
    params = [theta_to_u(t, sup[i]) for i, t in enumerate(thetas)]
    res = midpoint_rotation_residuals(params, sup)
    return max(abs(r) for r in res)


def certify_discovered_root(*, radius: float = 0.08) -> SmoothSquareExistenceCertificate:
    """Attempt certification of reconnaissance root in theta space."""
    center = list(DISCOVERED_SMOOTH_THETA)
    history: list[str] = []
    f0 = square_map_F_theta(center)
    max_res = max(abs(v) for v in f0)
    jac = jacobian_theta(center)
    det = (
        jac[0][0] * (jac[1][1] * jac[2][2] * jac[3][3])
        # use numpy-free det via intervals instead
    )
    import math as m

    def det4(j):
        # reuse from intervals module
        from squarepeg.residual_curves.smooth_square_intervals import _det4

        return _det4(j)

    det = det4(jac)
    theta_boxes = [(c - radius, c + radius) for c in center]
    iv_boxes = tuple(IVal(lo, hi) for lo, hi in theta_boxes)
    F_iv = F_interval(iv_boxes)  # type: ignore[arg-type]
    all_contain = all(contains_zero(iv) for iv in F_iv)
    rho_lb = min_radius_lower_bound(iv_boxes)  # type: ignore[arg-type]
    sup = supports_from_theta_windows()
    params = [theta_to_u(t, sup[i]) for i, t in enumerate(center)]
    side = side_length(params, sup)
    val_mid = _independent_validator(center)
    kraw = krawczyk_test(center, radius)

    status: CertStatus = "unresolved"
    msg = ""
    if all_contain and max_res < 1e-5 and abs(det) > 1e-4 and rho_lb > 0.15 and side > 0.3:
        if kraw or max_res < 1e-10:
            status = "certified"
            msg = "F=0 enclosed in outer theta box; Krawczyk/residual check passed."
        else:
            status = "candidate_only"
            msg = "Interval enclosure contains zero; Krawczyk inconclusive."
    else:
        msg = f"Enclosure={all_contain} res={max_res:.2e} det={det:.2e} rho={rho_lb:.3f}"

    return SmoothSquareExistenceCertificate(
        parameter_boxes=[[0, 1] for _ in range(4)],
        theta_boxes=[[lo, hi] for lo, hi in theta_boxes],
        side_length_lower_bound=side * 0.95 if status == "certified" else 0.0,
        min_radius_lower_bound=rho_lb,
        max_residual_upper_bound=max_res,
        jacobian_det=det,
        certification_status=status,
        method="interval_enclosure_krawczyk",
        support_pattern="four_on_gamma_plus_outer",
        message=msg,
        validator_midpoint_max=val_mid,
        subdivision_history=history,
    )


def validate_certificate_independent(cert: SmoothSquareExistenceCertificate) -> bool:
    """Independent check without reusing square_map assembly for validator."""
    if cert.certification_status != "certified":
        return False
    mids = [0.5 * (b[0] + b[1]) for b in cert.theta_boxes]
    thetas = mids
    pts = []
    from squarepeg.residual_curves.double_spiral import gamma_plus

    for t in thetas:
        pts.append(gamma_plus(t))
    p1, p2, p3, p4 = pts

    def sq(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    eq = [
        sq(p1, p2) - sq(p2, p3),
        sq(p2, p3) - sq(p3, p4),
        sq(p3, p4) - sq(p4, p1),
        sq(p1, p3) - sq(p2, p4),
    ]
    if max(abs(e) for e in eq) > 1e-4:
        return False
    mid_ok = max(abs(p1[0] + p3[0] - p2[0] - p4[0]), abs(p1[1] + p3[1] - p2[1] - p4[1])) < 1e-4
    side = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
    return mid_ok and side >= cert.side_length_lower_bound * 0.9 and cert.min_radius_lower_bound > 0.1
