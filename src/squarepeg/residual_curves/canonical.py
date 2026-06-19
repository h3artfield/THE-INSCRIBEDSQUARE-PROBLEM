"""Canonical double-spiral Jordan curve — frozen parameters (Directive 011)."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from squarepeg.residual_curves.double_spiral import (
    d_separation,
    gamma_minus,
    gamma_plus,
    r_outer,
)

Point = tuple[float, float]

# Frozen constants — do not change without new release tag.
CANONICAL_THETA0: float = 2.0 * math.pi
CANONICAL_EPS: Fraction = Fraction(1, 20)
CANONICAL_EPS_FLOAT: float = float(CANONICAL_EPS)
CANONICAL_ORIENTATION: Literal["ccw"] = "ccw"
# Parameter seam: u=0 at outer-arm outer endpoint gamma_+(theta0).
PARAM_SEAM_U: float = 0.0


def outer_connector_point(t: float, theta0: float = CANONICAL_THETA0) -> Point:
    """Connector at fixed outer radius: linear blend between arm endpoints at theta0."""
    p_plus = gamma_plus(theta0)
    p_minus = gamma_minus(theta0, CANONICAL_EPS_FLOAT)
    return (
        (1.0 - t) * p_minus[0] + t * p_plus[0],
        (1.0 - t) * p_minus[1] + t * p_plus[1],
    )


def theta_to_outer_arm_u(theta: float, theta0: float = CANONICAL_THETA0) -> float:
    """
    Circle parameter on outer arm: u=1 at theta0 (outer end), u->0 as theta->infty.
    u(theta) = r(theta)/r(theta0).
    """
    return r_outer(theta) / r_outer(theta0)


def outer_arm_u_to_theta(u: float, theta0: float = CANONICAL_THETA0) -> float:
    """Inverse: r = u*r0 => (1+theta)^(-1/2) = u*r0 => theta = (u*r0)^(-2)-1."""
    if u <= 0.0:
        return float("inf")
    r0 = r_outer(theta0)
    r = u * r0
    if r <= 0.0:
        return float("inf")
    return r ** (-2.0) - 1.0


def smooth_relative_area_outer_arm(m: float, n: float) -> float:
    """
    Relative antisymmetric area on outer arm segment [m, n] (m < n):
    (1/2) int_m^n r(theta)^2 dtheta minus endpoint chord correction.
    """
    if n <= m:
        return 0.0
    integral = 0.5 * math.log((1.0 + n) / (1.0 + m))
    pm = gamma_plus(m)
    pn = gamma_plus(n)
    chord = 0.5 * (pm[0] * pn[1] - pn[0] * pm[1])
    return integral - chord


def tail_interval_u(m: float, n: float) -> tuple[float, float]:
    """Parameter interval I = [t(N), t(M)] with t outer=1, inner=0."""
    return (theta_to_outer_arm_u(n), theta_to_outer_arm_u(m))


def tail_interval_length(m: float, n: float) -> float:
    u_lo, u_hi = tail_interval_u(m, n)
    return abs(u_hi - u_lo)


def tail_disk_radius(n: float) -> float:
    return r_outer(n)


@dataclass(frozen=True)
class CanonicalDoubleSpiral:
    """Frozen canonical double-spiral model."""

    theta0: float = CANONICAL_THETA0
    eps: Fraction = CANONICAL_EPS

    @property
    def eps_float(self) -> float:
        return float(self.eps)

    def outer_endpoint(self) -> Point:
        return gamma_plus(self.theta0)

    def inner_outer_endpoint(self) -> Point:
        return gamma_minus(self.theta0, self.eps_float)

    def definition_hash(self) -> str:
        payload = {
            "theta0": str(self.theta0),
            "eps": str(self.eps),
            "orientation": CANONICAL_ORIENTATION,
            "connector": "linear_chord_at_theta0",
            "param_seam": PARAM_SEAM_U,
            "r_formula": "(1+theta)^(-1/2)",
            "d_formula": "eps*(1+theta)^(-2)",
        }
        raw = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

    def truncated_polygon(self, turns: int) -> list[Point]:
        """Simple PL truncation: outer arm in, origin, inner arm out, outer connector."""
        from squarepeg.residual_curves.double_spiral import TruncatedDoubleSpiral

        t = TruncatedDoubleSpiral(
            turns=turns, eps=self.eps_float, theta0=self.theta0
        )
        outer = t.outer_vertices()
        inner = t.inner_vertices()
        conn = [self.inner_outer_endpoint(), self.outer_endpoint()]
        return outer + [(0.0, 0.0)] + inner + conn[0:1]

    def closed_polygon_with_connector(self, turns: int) -> list[Point]:
        """Full closed walk including connector back to start."""
        from squarepeg.residual_curves.double_spiral import TruncatedDoubleSpiral

        t = TruncatedDoubleSpiral(
            turns=turns, eps=self.eps_float, theta0=self.theta0
        )
        outer = t.outer_vertices()
        inner = t.inner_vertices()
        return outer + [(0.0, 0.0)] + inner + [
            self.inner_outer_endpoint(),
            self.outer_endpoint(),
        ]
