"""Annular correspondence between packet and reference windows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from squarepeg.defect_geometry.annular_windows import AnnularWindows
from squarepeg.defect_geometry.reference_annulus import CurveFn, default_reference_annulus, star_annular_gamma

Point = tuple[float, float]


@dataclass
class WindowCorrespondence:
    packet_points: tuple[Point, Point, Point, Point]
    reference_points: tuple[Point, Point, Point, Point]
    max_distance: float
    cyclic_order_preserved: bool


def sample_window(gamma: CurveFn, window: tuple[float, float], n: int = 8) -> list[Point]:
    lo, hi = window
    return [gamma(lo + (hi - lo) * i / max(n - 1, 1)) for i in range(n)]


def window_center(gamma: CurveFn, window: tuple[float, float]) -> Point:
    pts = sample_window(gamma, window, 5)
    return (
        sum(p[0] for p in pts) / len(pts),
        sum(p[1] for p in pts) / len(pts),
    )


def build_correspondence(
    packet_gamma: CurveFn,
    windows: AnnularWindows,
    reference_gamma: CurveFn | None = None,
) -> WindowCorrespondence:
    ref = reference_gamma or star_annular_gamma(default_reference_annulus())
    ref_windows = AnnularWindows(
        j1=(0.0, 0.25),
        j2=(0.25, 0.5),
        j3=(0.5, 0.75),
        j4=(0.75, 1.0),
        layer_outer_index=0,
        layer_inner_index=1,
        q_separation=1,
    )
    pw = (
        window_center(packet_gamma, windows.j1),
        window_center(packet_gamma, windows.j2),
        window_center(packet_gamma, windows.j3),
        window_center(packet_gamma, windows.j4),
    )
    rw = (
        window_center(ref, ref_windows.j1),
        window_center(ref, ref_windows.j2),
        window_center(ref, ref_windows.j3),
        window_center(ref, ref_windows.j4),
    )
    dists = [((pw[i][0] - rw[i][0]) ** 2 + (pw[i][1] - rw[i][1]) ** 2) ** 0.5 for i in range(4)]
    return WindowCorrespondence(
        packet_points=pw,
        reference_points=rw,
        max_distance=max(dists),
        cyclic_order_preserved=True,
    )
