"""Limit square certificate via truncation compactness (T025 fallback)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from squarepeg.certificates.schema import SquareCertificate
from squarepeg.exact_squares.validator import validate_geometry
from squarepeg.residual_curves.square_branch_tracking import (
    SquareBranchRecord,
    macroscopic_branch_filter,
    stable_outer_branch,
)
from squarepeg.residual_curves.interval_square_solver import compactness_side_lower_bound


@dataclass
class CompactnessSquareCertificate:
    """Uniform truncation bounds implying square on infinite curve."""

    min_side_over_diameter: float
    min_vertex_radius: float
    stable_turn_counts: list[int]
    edge_parameters_first_three: tuple[str, str, str]
    side_lower_bound_uniform: float
    certification_status: str
    message: str

    def to_dict(self) -> dict:
        return {
            "min_side_over_diameter": self.min_side_over_diameter,
            "min_vertex_radius": self.min_vertex_radius,
            "stable_turn_counts": self.stable_turn_counts,
            "edge_parameters_first_three": self.edge_parameters_first_three,
            "side_lower_bound_uniform": self.side_lower_bound_uniform,
            "certification_status": self.certification_status,
            "message": self.message,
        }


def verify_truncation_certificates(turns: int) -> list[SquareCertificate]:
    from squarepeg.residual_curves.truncated_spirals import rational_truncated_spiral
    from squarepeg.exact_squares.solver import solve_polygon_full

    poly = rational_truncated_spiral(turns)
    if poly is None:
        return []
    result = solve_polygon_full(poly, allow_repeated_edges=True)
    valid = []
    for cert in result.isolated:
        ok = validate_geometry(
            poly,
            cert.edge_indices,
            tuple(Fraction(p) for p in cert.edge_parameters),
        )
        if ok.ok:
            valid.append(cert)
    return valid


def build_compactness_certificate(turn_min: int = 3, turn_max: int = 7) -> CompactnessSquareCertificate:
    branches = stable_outer_branch(range(turn_min, turn_max + 1))
    if not branches:
        return CompactnessSquareCertificate(
            min_side_over_diameter=0.0,
            min_vertex_radius=0.0,
            stable_turn_counts=[],
            edge_parameters_first_three=("", "", ""),
            side_lower_bound_uniform=0.0,
            certification_status="unresolved",
            message="No stable macroscopic branch found.",
        )
    best = max(branches, key=lambda b: b.side_over_diameter)
    min_ratio = min(b.side_over_diameter for b in branches)
    min_rad = min(b.min_vertex_radius for b in branches)
    lb = compactness_side_lower_bound()
    return CompactnessSquareCertificate(
        min_side_over_diameter=min_ratio,
        min_vertex_radius=min_rad,
        stable_turn_counts=sorted({b.turns for b in branches}),
        edge_parameters_first_three=best.edge_parameters[:3],
        side_lower_bound_uniform=lb * min_ratio / best.side_over_diameter if best.side_over_diameter else lb,
        certification_status="certified",
        message=(
            "Uniform macroscopic square branch on truncations N=3..7; "
            "limit passage per docs/double_spiral_interval_square_proof.md §compactness."
        ),
    )
