"""Controlled C^1 polygon smoothing — velocity-matched cubic (T018, Directive 007R)."""

from __future__ import annotations

from squarepeg.variation.cubic_corner_smoothing import (
    SmoothedPolygon,
    cubic_bezier_derivative_ds,
    cubic_bezier_eval,
    cubic_control_points,
    cubic_endpoint_velocity_a,
    cubic_endpoint_velocity_c,
    projection_witness,
    quadratic_bezier,
    remove_collinear_vertices,
    round_corners_c1_cubic,
    w_dot_derivative_positive,
)

round_corners_c1 = round_corners_c1_cubic

__all__ = [
    "SmoothedPolygon",
    "round_corners_c1",
    "round_corners_c1_cubic",
    "remove_collinear_vertices",
    "cubic_control_points",
    "cubic_bezier_eval",
    "quadratic_bezier",
]
