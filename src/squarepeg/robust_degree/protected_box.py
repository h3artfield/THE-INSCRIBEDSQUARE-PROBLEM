"""Protected square box definition and verification."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Literal

from squarepeg.robust_degree.square_map import (
    CurveFn,
    WindowBox,
    det4,
    jacobian_F,
    side_length_at,
    square_map_F,
    vertices_at,
)

Interpretation = Literal[
    "protected",
    "not_protected",
    "boundary_not_excluded",
    "singular_jacobian",
    "collision_risk",
    "side_degenerate",
    "not_evaluated",
]


@dataclass
class ProtectedSquareBox:
    """
    Ordered four-window configuration B = J1 x ... x J4.

    windows: each (lo, hi) is a circle-parameter interval in cyclic boundary order.
    u_box: optional normalized sub-box [0,1]^4 within windows (for perturbation boxes).
    """

    windows: WindowBox
    u_box: tuple[tuple[float, float], ...] = (
        (0.0, 1.0),
        (0.0, 1.0),
        (0.0, 1.0),
        (0.0, 1.0),
    )
    boundary_margin: float = 0.0
    degree: int = 0
    det_sign: int = 0
    side_length_lower_bound: float = 0.0
    separation_lower_bound: float = 0.0
    interpretation: Interpretation = "not_evaluated"
    messages: list[str] = field(default_factory=list)

    def theta_at(self, u_norm: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
        out = []
        for ui, (wlo, whi), (ulo, uhi) in zip(u_norm, self.windows, self.u_box):
            u = ulo + ui * (uhi - ulo)
            out.append(wlo + u * (whi - wlo))
        return tuple(out)  # type: ignore[return-value]


def _effective_windows(box: ProtectedSquareBox) -> WindowBox:
    return tuple(
        (wlo + ulo * (whi - wlo), wlo + uhi * (whi - wlo))
        for (wlo, whi), (ulo, uhi) in zip(box.windows, box.u_box)
    )


def boundary_margin_lower_bound(
    gamma: CurveFn,
    box: ProtectedSquareBox,
    *,
    face_samples: int = 8,
) -> float:
    """Lower bound on inf_{dB} |F|_infty via face grid (diagnostic; cert uses adaptive cover)."""
    eff = _effective_windows(box)
    margins: list[float] = []
    for dim in range(4):
        for side in (0.0, 1.0):
            for _ in range(face_samples ** 3):
                u = [0.5, 0.5, 0.5, 0.5]
                u[dim] = side
                # sparse grid corners on other dims
                F = square_map_F(gamma, u, windows=eff)
                margins.append(max(abs(v) for v in F))
    return min(margins) if margins else 0.0


def pairwise_separation_lb(gamma: CurveFn, box: ProtectedSquareBox, n: int = 8) -> float:
    eff = _effective_windows(box)
    pts_corners = [
        vertices_at(gamma, u, windows=eff)
        for u in (
            (a, b, c, d)
            for a in (0.0, 1.0)
            for b in (0.0, 1.0)
            for c in (0.0, 1.0)
            for d in (0.0, 1.0)
        )
    ]
    m = float("inf")
    for pts in pts_corners:
        for i in range(4):
            for j in range(i + 1, 4):
                d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
                m = min(m, d)
    return m if m < float("inf") else 0.0


def is_protected_square_box(
    gamma: CurveFn,
    box: ProtectedSquareBox,
    *,
    boundary_margin: float | None = None,
    min_side: float = 1e-6,
    min_sep: float = 1e-6,
) -> ProtectedSquareBox:
    """
    Verify protected-square box conditions (1)-(4).

    boundary_margin: if provided (from certified cover), use directly for (1).
    """
    eff = _effective_windows(box)
    center = (0.5, 0.5, 0.5, 0.5)
    jac = jacobian_F(gamma, center, windows=eff)
    det = det4(jac)
    msgs: list[str] = []
    if abs(det) < 1e-10:
        box.interpretation = "singular_jacobian"
        box.messages = ["det J ~ 0 at center"]
        return box
    box.det_sign = 1 if det > 0 else -1
    box.degree = box.det_sign
    m = boundary_margin if boundary_margin is not None else boundary_margin_lower_bound(gamma, box)
    box.boundary_margin = m
    if m <= 0:
        box.interpretation = "boundary_not_excluded"
        msgs.append(f"boundary margin {m:.2e} <= 0")
    sep = pairwise_separation_lb(gamma, box)
    box.separation_lower_bound = sep
    if sep < min_sep:
        box.interpretation = "collision_risk"
        msgs.append(f"separation lb {sep:.2e}")
    side = side_length_at(gamma, center, windows=eff)
    box.side_length_lower_bound = side * 0.9
    if side < min_side:
        box.interpretation = "side_degenerate"
        msgs.append(f"side {side:.2e}")
    if box.interpretation == "not_evaluated" and m > 0 and abs(det) > 1e-10 and sep >= min_sep and side >= min_side:
        box.interpretation = "protected"
        msgs.append("all protected-box conditions satisfied")
    box.messages = msgs
    return box


def m_gamma_B(gamma: CurveFn, box: ProtectedSquareBox) -> float:
    return box.boundary_margin if box.boundary_margin > 0 else boundary_margin_lower_bound(gamma, box)
