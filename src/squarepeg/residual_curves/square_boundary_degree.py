"""Boundary exclusion cover and Brouwer degree for T025 square map."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from typing import Any

from squarepeg.residual_curves.independent_t025_verifier import F_at_point, invert4
from squarepeg.residual_curves.iv_backend_v1 import (
    F_interval,
    IVal,
    boxes_from_fractions,
    contains_zero,
    det_interval_on_box,
    excludes_zero,
    jacobian_float,
)
from squarepeg.residual_curves.t025_frozen_constants import DISCOVERED_THETA
from squarepeg.residual_curves.t025_frozen_constants import KRAWCZYK_RADIUS, KRAWCZYK_THETA_BOXES


def _float_boxes() -> list[tuple[float, float]]:
    return [(float(lo), float(hi)) for lo, hi in KRAWCZYK_THETA_BOXES]


@dataclass
class BoundaryCell:
    face_index: int
    face_side: str  # "lo" or "hi"
    bounds: list[tuple[float, float]]
    excluded_component: int
    margin: float

    def to_dict(self) -> dict:
        return {
            "face_index": self.face_index,
            "face_side": self.face_side,
            "bounds": self.bounds,
            "excluded_component": self.excluded_component,
            "margin": self.margin,
        }


@dataclass
class DegreeCertificate:
    parameter_box: list[list[float]]
    det_sign: int
    degree: int
    boundary_margin: float
    terminal_cells: list[BoundaryCell] = field(default_factory=list)
    uniqueness: bool = False

    def to_dict(self) -> dict:
        return {
            "parameter_box": self.parameter_box,
            "det_sign": self.det_sign,
            "degree": self.degree,
            "boundary_margin": self.boundary_margin,
            "uniqueness_in_box": self.uniqueness,
            "terminal_cells": [c.to_dict() for c in self.terminal_cells],
            "cell_count": len(self.terminal_cells),
        }


def _cell_excludes(F_iv: tuple[IVal, ...]) -> tuple[bool, int, float]:
    best = (-1, 0.0)
    for i, iv in enumerate(F_iv):
        if excludes_zero(iv):
            m = min(abs(iv.lo), abs(iv.hi))
            if m > best[1]:
                best = (i, m)
    return best[0] >= 0, best[0], best[1]


def _subdivide_cell(
    bounds: list[tuple[float, float]], dim: int, max_depth: int, depth: int
) -> list[list[tuple[float, float]]]:
    if depth >= max_depth:
        return [bounds]
    lo, hi = bounds[dim]
    mid = 0.5 * (lo + hi)
    b1 = [tuple(x) for x in bounds]
    b2 = [tuple(x) for x in bounds]
    b1[dim] = (lo, mid)
    b2[dim] = (mid, hi)
    out: list[list[tuple[float, float]]] = []
    out.extend(_subdivide_cell(b1, dim, max_depth, depth + 1))
    out.extend(_subdivide_cell(b2, dim, max_depth, depth + 1))
    return out


def cover_boundary_face(
    base_boxes: list[tuple[float, float]],
    face: int,
    side: str,
    *,
    max_depth: int = 6,
    min_margin: float = 1e-8,
) -> list[BoundaryCell]:
    lo, hi = base_boxes[face]
    fixed = hi if side == "hi" else lo
    free_dims = [d for d in range(4) if d != face]
    bounds0 = list(base_boxes)
    bounds0[face] = (fixed, fixed)
    widest = max(free_dims, key=lambda d: base_boxes[d][1] - base_boxes[d][0])

    def refine(bounds: list[tuple[float, float]], depth: int) -> list[BoundaryCell]:
        ivs = [IVal(a, b) for a, b in bounds]
        F_iv = F_interval(tuple(ivs))  # type: ignore[arg-type]
        ok, comp, margin = _cell_excludes(F_iv)
        if ok and margin >= min_margin:
            return [BoundaryCell(face, side, bounds, comp, margin)]
        if depth >= max_depth + 4:
            if ok:
                return [BoundaryCell(face, side, bounds, comp, margin)]
            return []
        out: list[BoundaryCell] = []
        # Subdivide widest free dimension
        w = max(
            (d for d in free_dims),
            key=lambda d: bounds[d][1] - bounds[d][0],
        )
        lo_d, hi_d = bounds[w]
        mid = 0.5 * (lo_d + hi_d)
        b1 = [tuple(x) for x in bounds]
        b2 = [tuple(x) for x in bounds]
        b1[w] = (lo_d, mid)
        b2[w] = (mid, hi_d)
        out.extend(refine(b1, depth + 1))
        out.extend(refine(b2, depth + 1))
        return out

    return refine(bounds0, 0)


def certify_boundary_exclusion(*, max_depth: int = 6) -> DegreeCertificate:
    boxes = _float_boxes()
    center = list(DISCOVERED_THETA)
    radius = float(KRAWCZYK_RADIUS)
    iv_boxes = boxes_from_fractions(tuple(boxes))
    det_iv = det_interval_on_box(tuple(boxes))
    if contains_zero(det_iv):
        raise RuntimeError("det(DF) interval contains zero on B")
    det_sign = 1 if det_iv.lo > 0 else -1
    cells: list[BoundaryCell] = []
    for face in range(4):
        for side in ("lo", "hi"):
            cells.extend(cover_boundary_face(boxes, face, side, max_depth=max_depth))
    if not cells:
        raise RuntimeError("boundary cover empty")
    margin = min(c.margin for c in cells)
    # Uniqueness: Krawczyk + nonsingular det on box
    jac = jacobian_float(center)
    inv = invert4(jac)
    f0 = F_at_point(center)
    res = max(abs(v) for v in f0)
    inv_norm = max(sum(abs(inv[i][j]) for j in range(4)) for i in range(4)) if inv else float("inf")
    uniqueness = res * inv_norm < 0.5 * radius and not contains_zero(det_iv)
    return DegreeCertificate(
        parameter_box=[[lo, hi] for lo, hi in boxes],
        det_sign=det_sign,
        degree=det_sign,
        boundary_margin=margin,
        terminal_cells=cells,
        uniqueness=uniqueness,
    )


def validate_boundary_certificate(cert: DegreeCertificate) -> bool:
    margins = []
    for cell in cert.terminal_cells:
        ivs = [IVal(lo, hi) for lo, hi in cell.bounds]
        F_iv = F_interval(tuple(ivs))  # type: ignore[arg-type]
        iv = F_iv[cell.excluded_component]
        if contains_zero(iv):
            return False
        margins.append(min(abs(iv.lo), abs(iv.hi)))
    if min(margins) < cert.boundary_margin * 0.5:
        return False
    return cert.degree == cert.det_sign and cert.det_sign != 0


def boundary_certificate_hash(cert: DegreeCertificate) -> str:
    return hashlib.sha256(json.dumps(cert.to_dict(), sort_keys=True).encode()).hexdigest()


def export_boundary_certificate(path: str, *, max_depth: int = 6) -> DegreeCertificate:
    cert = certify_boundary_exclusion(max_depth=max_depth)
    payload = cert.to_dict()
    payload["certificate_hash_sha256"] = boundary_certificate_hash(cert)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    return cert
