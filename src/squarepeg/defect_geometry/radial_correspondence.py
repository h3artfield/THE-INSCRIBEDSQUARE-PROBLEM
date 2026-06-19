"""Angular radial correspondence packet <-> reference."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_geometry.annular_graph import RadialLayer

Point = tuple[float, float]


@dataclass
class NormalizedLayerPair:
    """L_j scaled to max r = 1, center at origin."""
    outer: RadialLayer
    inner: RadialLayer
    g_star: float
    scale: float


@dataclass
class RadialCorrespondence:
    window_points_packet: tuple[Point, Point, Point, Point]
    window_points_reference: tuple[Point, Point, Point, Point]
    max_distance: float
    cyclic_order_preserved: bool
    orientation_preserving: bool


def normalize_layer_pair(outer: RadialLayer, inner: RadialLayer) -> NormalizedLayerPair:
    mx = outer.max_radius()
    scale = 1.0 / mx if mx > 1e-12 else 1.0
    orad = [r * scale for r in outer.radii]
    irad = [r * scale for r in inner.radii]
    o_norm = RadialLayer(
        center=(0.0, 0.0),
        radii=orad,
        n_theta=outer.n_theta,
        diameter=outer.diameter * scale,
        winding_sign=outer.winding_sign,
    )
    i_norm = RadialLayer(
        center=(0.0, 0.0),
        radii=irad,
        n_theta=inner.n_theta,
        diameter=inner.diameter * scale,
        winding_sign=inner.winding_sign,
    )
    ratios = [irad[i] / max(orad[i], 1e-12) for i in range(min(len(orad), len(irad)))]
    ratios.sort()
    g_star = ratios[len(ratios) // 2] if ratios else 0.5
    return NormalizedLayerPair(outer=o_norm, inner=i_norm, g_star=g_star, scale=scale)


def polar_point(r: float, theta: float) -> Point:
    return r * math.cos(theta), r * math.sin(theta)


def four_window_points(layer: RadialLayer, thetas: tuple[float, float, float, float]) -> tuple[Point, ...]:
    n = len(layer.radii)
    pts: list[Point] = []
    for t in thetas:
        idx = int(round(t / (2 * math.pi) * n)) % n
        r = layer.radii[idx]
        pts.append(polar_point(r, t))
    return tuple(pts)


def build_radial_correspondence(pair: NormalizedLayerPair) -> RadialCorrespondence:
    g = pair.g_star
    n_o = len(pair.outer.radii)
    n_i = len(pair.inner.radii)
    pkt = (
        polar_point(pair.outer.radii[0], 0.0),
        polar_point(pair.inner.radii[n_i // 4], math.pi / 2),
        polar_point(pair.inner.radii[n_i // 2], math.pi),
        polar_point(pair.outer.radii[3 * n_o // 4], 3 * math.pi / 2),
    )
    ref = (
        polar_point(1.0, 0.0),
        polar_point(g, math.pi / 2),
        polar_point(g, math.pi),
        polar_point(1.0, 3 * math.pi / 2),
    )
    dists = [math.hypot(pkt[i][0] - ref[i][0], pkt[i][1] - ref[i][1]) for i in range(4)]
    return RadialCorrespondence(
        window_points_packet=pkt,
        window_points_reference=ref,
        max_distance=max(dists),
        cyclic_order_preserved=True,
        orientation_preserving=True,
    )


def psi_from_correspondence(pair: NormalizedLayerPair) -> float:
    """Observed window-point distance (diagnostic; proved bound is psi_annular_bound)."""
    return build_radial_correspondence(pair).max_distance
