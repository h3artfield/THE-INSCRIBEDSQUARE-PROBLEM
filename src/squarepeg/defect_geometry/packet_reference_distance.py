"""Packet-to-reference distance Psi and T036-N1 comparison."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_geometry.annular_correspondence import build_correspondence
from squarepeg.defect_geometry.annular_windows import AnnularWindows, extract_windows
from squarepeg.defect_geometry.lobe_tree import LobeTree
from squarepeg.defect_geometry.nested_chain import NestedClassParams, find_same_sign_chain
from squarepeg.defect_geometry.reference_cyclic_certificate import rho_cyc_reference


@dataclass
class ComparisonBound:
    psi: float
    rho_cyc: float
    closeness_sufficient: bool
    missing_hypothesis: str | None


def psi_estimate(
    m: int,
    lambda_minus: float,
    lambda_plus: float,
    delta_sep: float,
    beta: float,
    q0: int,
) -> float:
    """
    Crude geometric bound: nesting depth m with scale ratio lambda+ gives
    outer-inner separation; eccentricity and corridor twist add O(1/m).
    """
    scale_spread = lambda_plus - lambda_minus
    depth_penalty = (1.0 - lambda_minus) ** max(m - 1, 0)
    sep_term = max(0.0, 1.0 - delta_sep * m)
    return scale_spread + depth_penalty + 1.0 / max(m, 1) + (1.0 - beta) * 0.5


def compare_packet_to_reference(
    tree: LobeTree,
    params: NestedClassParams | None = None,
    packet_gamma=None,
) -> ComparisonBound:
    p = params or NestedClassParams()
    chain = find_same_sign_chain(tree)
    m = chain.depth
    psi = psi_estimate(m, p.lambda_minus, p.lambda_plus, p.delta_sep, p.beta, q0=1)
    rho = rho_cyc_reference()
    sufficient = psi < rho if rho > 0 else False
    missing = None
    if not sufficient:
        missing = (
            "Nesting constants alone do not force Psi < rho_cyc; need ANNULAR_GRAPH or "
            "bounded_eccentricity hypothesis on attachment corridors"
        )
    return ComparisonBound(psi=psi, rho_cyc=rho, closeness_sufficient=sufficient, missing_hypothesis=missing)


def t036_n1_conditional_theorem() -> str:
    return (
        "T036-N1 (conditional): If normalized packet in D_nest has four windows with "
        "Psi(packet, Gamma_ref) < rho_cyc(Gamma_ref), then a cyclic-odd protected rhombus "
        "component exists at outer scale; T039 yields a square with side >= c_sq d_{L_j}."
    )
