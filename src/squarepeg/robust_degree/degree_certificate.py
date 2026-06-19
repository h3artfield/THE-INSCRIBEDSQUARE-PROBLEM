"""Degree certificates for protected square boxes."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

from squarepeg.robust_degree.protected_box import ProtectedSquareBox, is_protected_square_box
from squarepeg.robust_degree.square_map import CurveFn, det4, jacobian_F


@dataclass
class DegreeCertificate:
    windows: list[list[float]]
    u_box: list[list[float]]
    degree: int
    det_sign: int
    boundary_margin: float
    side_length_lower_bound: float
    separation_lower_bound: float
    source: str = "abstract"
    terminal_boundary_cells: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def certificate_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True).encode()).hexdigest()


def from_protected_box(box: ProtectedSquareBox) -> DegreeCertificate:
    return DegreeCertificate(
        windows=[[a, b] for a, b in box.windows],
        u_box=[[a, b] for a, b in box.u_box],
        degree=box.degree,
        det_sign=box.det_sign,
        boundary_margin=box.boundary_margin,
        side_length_lower_bound=box.side_length_lower_bound,
        separation_lower_bound=box.separation_lower_bound,
        source="protected_box",
    )


def from_t025_boundary_cert(boundary_payload: dict[str, Any]) -> DegreeCertificate:
    return DegreeCertificate(
        windows=boundary_payload["parameter_box"],
        u_box=[[0, 1]] * 4,
        degree=boundary_payload["degree"],
        det_sign=boundary_payload["det_sign"],
        boundary_margin=boundary_payload["boundary_margin"],
        side_length_lower_bound=0.355,
        separation_lower_bound=0.335,
        source="t025_boundary_exclusion",
        terminal_boundary_cells=boundary_payload.get("terminal_cells", []),
    )


def certify_degree(
    gamma: CurveFn,
    box: ProtectedSquareBox,
    *,
    boundary_margin: float | None = None,
) -> DegreeCertificate | None:
    checked = is_protected_square_box(gamma, box, boundary_margin=boundary_margin)
    if checked.interpretation != "protected":
        return None
    return from_protected_box(checked)


def square_exists_from_degree(cert: DegreeCertificate) -> bool:
    """T029 consequence: nonzero degree => zero exists."""
    return cert.degree != 0 and cert.boundary_margin > 0
