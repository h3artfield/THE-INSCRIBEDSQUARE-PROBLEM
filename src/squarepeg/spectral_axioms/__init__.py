"""Spectral axiom audit and midpoint nonflatness LP models."""

from squarepeg.spectral_axioms.continuum_verify import (
    certify_grid_witness,
    grid_pl_function,
    verify_subadditive_grid,
)
from squarepeg.spectral_axioms.grid_model import GridLPConfig, GridLPResult, solve_grid_lp
from squarepeg.spectral_axioms.normalization import (
    B_from_area_radius,
    kappa_from_B,
    midpoint_quotient,
    normalize_spectral,
)

__all__ = [
    "B_from_area_radius",
    "GridLPConfig",
    "GridLPResult",
    "certify_grid_witness",
    "grid_pl_function",
    "kappa_from_B",
    "midpoint_quotient",
    "normalize_spectral",
    "solve_grid_lp",
    "verify_subadditive_grid",
]
