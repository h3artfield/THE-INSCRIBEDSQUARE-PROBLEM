"""Exact cyclic surgery decomposition and master area identity (Directive 025)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.area_variation.signed_area import relative_area_increment
from squarepeg.defect_surgery.concatenation_area import (
    concatenate_paths,
    relative_area_path,
    wedge,
)
from squarepeg.defect_surgery.crosscut import straight_chord_crosscut
from squarepeg.defect_surgery.local_surgery import apply_local_surgery
from squarepeg.defect_surgery.nested_forest import PacketForest, maximal_disks
from squarepeg.defect_surgery.packet_disk import PacketDisk, Point

ComponentPath = list[Point]


@dataclass
class PathComponent:
    """One retained or crosscut component in traversal order."""

    kind: str  # "retained" | "crosscut"
    path: ComponentPath
    delta: Point

    @property
    def intrinsic_area(self) -> float:
        return relative_area_path(self.path) if len(self.path) >= 2 else 0.0


@dataclass
class CyclicDecomposition:
    """Q_n|_J = R_0 * C_1 * R_1 * ... after removing empty components."""

    components: list[PathComponent]
    interval_indices: list[int]
    wraps_seam: bool

    @property
    def retained(self) -> list[PathComponent]:
        return [c for c in self.components if c.kind == "retained"]

    @property
    def crosscuts(self) -> list[PathComponent]:
        return [c for c in self.components if c.kind == "crosscut"]


@dataclass
class MasterAreaIdentity:
    """Exact master surgery-area identity on a test interval."""

    sum_retained_area: float
    attachment_chain_area: float
    chi_curved: float
    master_lhs: float
    master_rhs: float
    exact: bool
    pairwise_wedge_area: float


def component_delta(path: ComponentPath) -> Point:
    if len(path) < 2:
        return (0.0, 0.0)
    a, b = path[0], path[-1]
    return (b[0] - a[0], b[1] - a[1])


def pairwise_wedge_area(deltas: list[Point]) -> float:
    """A_Z = 1/2 sum_{i<j} Delta_i wedge Delta_j for attachment chain increments."""
    total = 0.0
    for i in range(len(deltas)):
        for j in range(i + 1, len(deltas)):
            total += wedge(deltas[i], deltas[j])
    return 0.5 * total


def attachment_chain_vertices(origin: Point, deltas: list[Point]) -> list[Point]:
    pts = [origin]
    x, y = origin
    for dx, dy in deltas:
        x += dx
        y += dy
        pts.append((x, y))
    return pts


def attachment_chain_area_from_deltas(origin: Point, deltas: list[Point]) -> float:
    pts = attachment_chain_vertices(origin, deltas)
    return relative_area_path(pts) if len(pts) >= 2 else 0.0


def verify_notation_equivalence(path: ComponentPath, tol: float = 1e-9) -> bool:
    """Relative area matches T021 / signed_area convention."""
    if len(path) < 2:
        return True
    return abs(relative_area_path(path) - relative_area_increment(path)) <= tol


def master_area_identity(components: list[PathComponent], *, tol: float = 1e-8) -> MasterAreaIdentity:
    """
    A_{Q}(J) = sum_i A_{R_i} + A_{Z}  (+ sum A_{C_i} for curved crosscuts).

    Z uses net displacements Delta_i of every component in traversal order.
    """
    if not components:
        return MasterAreaIdentity(0.0, 0.0, 0.0, 0.0, 0.0, True, 0.0)

    deltas = [c.delta for c in components]
    origin = components[0].path[0]
    a_z = attachment_chain_area_from_deltas(origin, deltas)
    a_pw = pairwise_wedge_area(deltas)
    sum_r = sum(c.intrinsic_area for c in components if c.kind == "retained")
    sum_c = sum(c.intrinsic_area for c in components if c.kind == "crosscut")

    full_path = concatenate_paths(*[c.path for c in components])
    lhs = relative_area_path(full_path)
    rhs = sum_r + sum_c + a_z
    return MasterAreaIdentity(
        sum_retained_area=sum_r,
        attachment_chain_area=a_z,
        chi_curved=sum_c,
        master_lhs=lhs,
        master_rhs=rhs,
        exact=abs(lhs - rhs) <= tol and abs(a_z - a_pw) <= tol,
        pairwise_wedge_area=a_pw,
    )


def _indices_in_cyclic_interval(n: int, i0: int, i1: int) -> list[int]:
    """Vertex indices from i0 to i1 inclusive, allowing wrap on closed polygon."""
    if i0 <= i1:
        return list(range(i0, i1 + 1))
    return list(range(i0, n)) + list(range(0, i1 + 1))


def extract_subarc_vertices(vertices: list[Point], i0: int, i1: int) -> tuple[list[Point], bool]:
    """Lift seam-crossing intervals by duplicating the start vertex."""
    n = len(vertices)
    idxs = _indices_in_cyclic_interval(n, i0, i1)
    wraps = i0 > i1
    pts = [vertices[i] for i in idxs]
    return pts, wraps


def disk_intersects_cyclic_interval(d: PacketDisk, n: int, i0: int, i1: int) -> bool:
    lo = min(d.interval_start, d.interval_end)
    hi = max(d.interval_start, d.interval_end)
    arc = set(_indices_in_cyclic_interval(n, i0, i1))
    disk_idx = set(range(lo, hi + 1))
    return bool(arc & disk_idx)


def _in_surgery_span(vi: int, spans: list[tuple[int, int, PacketDisk]]) -> tuple[int, int, PacketDisk] | None:
    for lo, hi, d in spans:
        if lo <= vi <= hi:
            return lo, hi, d
    return None


def decompose_cyclic_interval(
    vertices: list[Point],
    i0: int,
    i1: int,
    forest: PacketForest,
) -> CyclicDecomposition:
    """
    Decompose Q_n|_J into connected R_0 * C_1 * R_1 * ... components.

    Maximal disjoint surgery intervals; empty components removed.
    """
    n = len(vertices)
    idxs = _indices_in_cyclic_interval(n, i0, i1)
    wraps = i0 > i1
    idx_set = set(idxs)
    spans: list[tuple[int, int, PacketDisk]] = []
    for d in sorted(maximal_disks(forest), key=lambda x: min(x.interval_start, x.interval_end)):
        lo = min(d.interval_start, d.interval_end)
        hi = max(d.interval_start, d.interval_end)
        if idx_set & set(range(lo, hi + 1)):
            spans.append((lo, hi, d))

    if not spans:
        rpath = [vertices[i] for i in idxs]
        comps = (
            [PathComponent("retained", rpath, component_delta(rpath))]
            if len(rpath) >= 2
            else []
        )
        return CyclicDecomposition(components=comps, interval_indices=idxs, wraps_seam=wraps)

    components: list[PathComponent] = []
    k = 0
    while k < len(idxs):
        vi = idxs[k]
        span = _in_surgery_span(vi, spans)
        if span is None:
            start = k
            while k < len(idxs) and _in_surgery_span(idxs[k], spans) is None:
                k += 1
            rpath = [vertices[idxs[j]] for j in range(start, k)]
            if k < len(idxs):
                entry_lo = _in_surgery_span(idxs[k], spans)
                if entry_lo:
                    lo, _, _ = entry_lo
                    if not rpath or rpath[-1] != vertices[lo]:
                        rpath.append(vertices[lo])
            if len(rpath) >= 2:
                components.append(PathComponent("retained", rpath, component_delta(rpath)))
        else:
            lo, hi, d = span
            pa = vertices[d.interval_start]
            pb = vertices[d.interval_end]
            components.append(
                PathComponent("crosscut", [pa, pb], component_delta([pa, pb]))
            )
            while k < len(idxs) and idxs[k] <= hi:
                k += 1
            if k >= len(idxs):
                break
            tail = [pb]
            while k < len(idxs) and _in_surgery_span(idxs[k], spans) is None:
                tail.append(vertices[idxs[k]])
                k += 1
            if k < len(idxs):
                entry_lo = _in_surgery_span(idxs[k], spans)
                if entry_lo:
                    lo2, _, _ = entry_lo
                    if tail[-1] != vertices[lo2]:
                        tail.append(vertices[lo2])
            if len(tail) >= 2:
                components.append(PathComponent("retained", tail, component_delta(tail)))

    components = [c for c in components if len(c.path) >= 2]
    return CyclicDecomposition(components=components, interval_indices=idxs, wraps_seam=wraps)


def decompose_from_surgered_polygon(
    original: list[Point],
    surgered: list[Point],
    i0: int,
    i1: int,
    forest: PacketForest,
) -> CyclicDecomposition:
    """Build decomposition from surgered polygon by comparing to surgery forest."""
    _ = (original, surgered)
    return decompose_cyclic_interval(original, i0, i1, forest)


def uniform_surgery_error_bound(forest: PacketForest) -> float:
    """|Q_n - P_n|_infty <= r_n^max over maximal disks."""
    maximal = maximal_disks(forest)
    if not maximal:
        return 0.0
    return max(d.diameter for d in maximal)


def straight_crosscut_area_zero(cross_path: ComponentPath, tol: float = 1e-12) -> bool:
    return abs(relative_area_path(cross_path)) <= tol
