"""Frozen T025 constants — shared by primary and independent paths."""

from __future__ import annotations

from fractions import Fraction

# Canonical model identifier (matches canonical.py hash payload).
CANONICAL_MODEL_ID = "gamma_plus_outer_v1_theta0_2pi_eps_1_20"
CANONICAL_CURVE_HASH = "c535f4e3cc643ed945854ba53d818444245e00c014648625b8603c344d648ae7"

SUPPORT_PIECE_IDS = ("gamma_plus_J1", "gamma_plus_J2", "gamma_plus_J3", "gamma_plus_J4")

# Certified support windows J_i (theta on gamma_+).
SUPPORT_THETA_INTERVALS: tuple[tuple[Fraction, Fraction], ...] = (
    (Fraction(575, 100), Fraction(605, 100)),
    (Fraction(1055, 100), Fraction(1100, 100)),
    (Fraction(1495, 100), Fraction(1535, 100)),
    (Fraction(705, 100), Fraction(745, 100)),
)

# Krawczyk / degree box B: center ± 3/20 in each coordinate (radius 0.15).
KRAWCZYK_RADIUS = Fraction(3, 20)

# Reconnaissance root (optional metadata only — proofs use intervals).
DISCOVERED_THETA: tuple[float, float, float, float] = (
    5.904664570522921,
    10.768443130208531,
    15.133643385520857,
    7.207559275277679,
)

KRAWCZYK_CENTERS = DISCOVERED_THETA

KRAWCZYK_THETA_BOXES: tuple[tuple[Fraction, Fraction], ...] = tuple(
    (
        Fraction(c).limit_denominator(10**12) - KRAWCZYK_RADIUS,
        Fraction(c).limit_denominator(10**12) + KRAWCZYK_RADIUS,
    )
    for c in DISCOVERED_THETA
)

INTERVAL_LIBRARY = "squarepeg.residual_curves.iv_backend_v1"
ROUNDING_MODE = "outward_float_enclosure"

T025_STATUS = "PROVED_LOCALLY_BY_DIRECT_INTERVAL_CERTIFICATE"
