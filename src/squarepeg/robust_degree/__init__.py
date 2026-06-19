"""Robust square degree invariant — curve-independent protected-square theory."""

from squarepeg.robust_degree.area_defect import (
    alpha_P_delta,
    alpha_sequence_limsup,
    is_area_tight_sequence,
    polygon_gamma,
)
from squarepeg.robust_degree.blowup import analyze_blowup, local_dichotomy_prototype
from squarepeg.robust_degree.collapse_classifier import (
    CollapseMode,
    SequenceDiagnostic,
    diagnose_polygon_sequence,
    run_counterexample_search,
)
from squarepeg.robust_degree.degree_certificate import (
    DegreeCertificate,
    certify_degree,
    from_t025_boundary_cert,
    square_exists_from_degree,
)
from squarepeg.robust_degree.limit_persistence import (
    recover_t027_instance,
    t030_robust_openness,
    t031_positive_limsup_persistence,
)
from squarepeg.robust_degree.perturbation_radius import (
    E_gamma_B,
    rho_square_box,
    rho_square_curve,
)
from squarepeg.robust_degree.polygon_extractor import (
    ProtectedSquareCertificate,
    convert_isolated_square,
    rho_square_cert_polygon,
)
from squarepeg.robust_degree.protected_box import (
    ProtectedSquareBox,
    is_protected_square_box,
    m_gamma_B,
)
from squarepeg.robust_degree.square_map import square_map_F, jacobian_F, det4

__all__ = [
    "ProtectedSquareBox",
    "ProtectedSquareCertificate",
    "DegreeCertificate",
    "CollapseMode",
    "SequenceDiagnostic",
    "square_map_F",
    "is_protected_square_box",
    "certify_degree",
    "square_exists_from_degree",
    "E_gamma_B",
    "rho_square_box",
    "rho_square_curve",
    "t030_robust_openness",
    "t031_positive_limsup_persistence",
    "recover_t027_instance",
    "convert_isolated_square",
    "rho_square_cert_polygon",
    "alpha_P_delta",
    "diagnose_polygon_sequence",
    "run_counterexample_search",
    "analyze_blowup",
]
