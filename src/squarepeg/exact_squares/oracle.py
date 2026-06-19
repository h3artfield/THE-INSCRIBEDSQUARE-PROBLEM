"""Independent floating-point oracle for inscribed squares (testing only)."""

from __future__ import annotations

import itertools
import math
from typing import Iterator

import numpy as np

from squarepeg.curves.polygon import PolygonCurve


def _is_square(points: np.ndarray, tol: float = 1e-8) -> bool:
    p = points
    sides = [np.linalg.norm(p[(i + 1) % 4] - p[i]) for i in range(4)]
    if min(sides) < tol:
        return False
    if max(sides) - min(sides) > tol:
        return False
    d1 = np.linalg.norm(p[0] - p[2])
    d2 = np.linalg.norm(p[1] - p[3])
    if abs(d1 - d2) > tol:
        return False
    v1 = p[1] - p[0]
    v2 = p[2] - p[1]
    if abs(np.dot(v1, v2)) > tol * max(np.linalg.norm(v1), np.linalg.norm(v2), 1.0):
        return False
    return True


def _point_on_segment(p: np.ndarray, a: np.ndarray, b: np.ndarray, tol: float) -> bool:
    ab = b - a
    ap = p - a
    cross = abs(ab[0] * ap[1] - ab[1] * ap[0])
    if cross > tol * max(np.linalg.norm(ab), 1.0):
        return False
    dot = np.dot(ap, ab)
    if dot < -tol or dot > np.dot(ab, ab) + tol:
        return False
    return True


def _vertices_on_polygon(polygon: PolygonCurve, points: np.ndarray, tol: float) -> bool:
    verts = np.array([[float(x), float(y)] for x, y in polygon.vertices])
    n = len(verts)
    for p in points:
        ok = False
        for i in range(n):
            a = verts[i]
            b = verts[(i + 1) % n]
            if _point_on_segment(p, a, b, tol):
                ok = True
                break
        if not ok:
            return False
    return True


def _dedup_oracle(squares: list[np.ndarray], tol: float) -> list[np.ndarray]:
    keys: list[tuple] = []
    out: list[np.ndarray] = []
    for sq in squares:
        key = tuple(round(float(c), 8) for p in sq for c in p)
        rotations = [key[i * 2 :] + key[: i * 2] for i in range(4)]
        rev = [tuple(reversed(r)) for r in rotations]
        canon = min(rotations + rev)
        if canon not in keys:
            keys.append(canon)
            out.append(sq)
    return out


def oracle_squares_on_polygon(
    polygon: PolygonCurve,
    *,
    samples_per_edge: int = 20,
    tol: float = 1e-6,
) -> list[np.ndarray]:
    """
    Brute-force sample quadruples of boundary points; return distinct squares found.
    FOR TESTING ONLY — not a certificate source.
    """
    verts = np.array([[float(x), float(y)] for x, y in polygon.vertices])
    n = len(verts)
    boundary: list[np.ndarray] = []
    for i in range(n):
        a = verts[i]
        b = verts[(i + 1) % n]
        for t in np.linspace(0.0, 1.0, samples_per_edge, endpoint=True):
            boundary.append(a + t * (b - a))

    found: list[np.ndarray] = []
    for combo in itertools.combinations(range(len(boundary)), 4):
        pts = np.array([boundary[i] for i in combo])
        for perm in itertools.permutations(range(4)):
            ordered = pts[list(perm)]
            if not _is_square(ordered, tol):
                continue
            if not _vertices_on_polygon(polygon, ordered, tol):
                continue
            found.append(ordered)
            break

    return _dedup_oracle(found, tol)


def oracle_count_squares(polygon: PolygonCurve, **kwargs) -> int:
    return len(oracle_squares_on_polygon(polygon, **kwargs))
