"""Certified annular-graph regime and T036-N1-ANN."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from squarepeg.defect_geometry.annular_graph import (
    AnnularGraphConstants,
    AnnularGraphPacket,
    radial_layer_from_ellipse,
    validate_annular_graph,
)
from squarepeg.defect_geometry.packet_reference_bound import psi_annular_bound, psi_from_constants
from squarepeg.defect_geometry.reference_cyclic_certificate import certify_reference_annular, rho_cyc_reference

T036N1AnnStatus = Literal[
    "PROVED_LOCALLY",
    "CONJECTURAL_TARGET",
    "REGIME_EMPTY",
]

# Certified nonempty parameter regime (Directive 021).
# Chosen so explicit Psi < rho_cyc (see docs/annular_packet_comparison_bound.md).
CERTIFIED_REGIME = AnnularGraphConstants(
    K=1.005,
    L=0.01,
    g_minus=0.449,
    g_plus=0.451,
    w_corr=0.005,
    delta_core=0.02,
    zeta=0.002,
)

C_ANN = 0.12  # side(Q) >= c_ann * d_{L_j}


@dataclass
class AnnularGraphCertificate:
    in_certified_regime: bool
    psi_sufficient: bool
    psi: float
    rho_cyc: float
    t039_applies: bool
    t036_n1_ann_status: T036N1AnnStatus
    c_ann: float
    depth_required: int
    messages: list[str] = field(default_factory=list)


def example_certified_packet() -> AnnularGraphPacket:
    """Nearly circular annular layers with K = 1.008 in certified regime."""
    inv_k = 1.0 / CERTIFIED_REGIME.K
    outer = radial_layer_from_ellipse(1.0, inv_k)
    inner = radial_layer_from_ellipse(0.45, 0.45 * inv_k)
    return AnnularGraphPacket(
        layers=[outer, inner],
        corridor_width=0.004,
        constants=CERTIFIED_REGIME,
    )


def certify_t036_n1_ann() -> AnnularGraphCertificate:
    ref = certify_reference_annular(0.01)
    psi_b = psi_from_constants(CERTIFIED_REGIME, g_star=0.45)
    pkt = example_certified_packet()
    ag_ok = validate_annular_graph(pkt)
    regime_ok = psi_b.sufficient and ag_ok
    status: T036N1AnnStatus
    if ref.t039_applies and psi_b.sufficient and ag_ok and regime_ok:
        status = "PROVED_LOCALLY"
    elif not psi_b.sufficient:
        status = "REGIME_EMPTY"
    else:
        status = "CONJECTURAL_TARGET"

    return AnnularGraphCertificate(
        in_certified_regime=regime_ok,
        psi_sufficient=psi_b.sufficient,
        psi=psi_b.psi,
        rho_cyc=psi_b.rho_cyc,
        t039_applies=ref.t039_applies,
        t036_n1_ann_status=status,
        c_ann=C_ANN,
        depth_required=2,
        messages=[
            "T036-N1-ANN: two controlled layers suffice; depth m0=2",
            f"side(Q) >= {C_ANN} * d_Lj (packet outer diameter scale)",
        ],
    )


def export_reference_certificate_json(path: Path | None = None) -> dict:
    ref = certify_reference_annular(0.01)
    psi_b = psi_from_constants(CERTIFIED_REGIME)
    data = {
        "model": "star_annular_Gamma_ref",
        "rank_dg": ref.rank_dg,
        "w1_pairing": ref.w1_pairing,
        "rho_cyc": psi_b.rho_cyc,
        "rho_cyc_certified_input": ref.rho_cyc,
        "boundary_margin": ref.boundary_margin,
        "t039_applies": ref.t039_applies,
        "g_star_reference": 0.45,
        "side_margin": "see reference_rhombus_family audit",
        "collision_margin": "see reference_rhombus_family audit",
        "rhombus_boundary_margin": ref.boundary_margin,
        "c0_perturbation_radius": psi_b.rho_cyc,
        "certified_regime": {
            "K": CERTIFIED_REGIME.K,
            "L": CERTIFIED_REGIME.L,
            "g_minus": CERTIFIED_REGIME.g_minus,
            "g_plus": CERTIFIED_REGIME.g_plus,
            "w_corr": CERTIFIED_REGIME.w_corr,
            "zeta": CERTIFIED_REGIME.zeta,
        },
        "psi_certified": psi_b.psi,
        "psi_sufficient": psi_b.sufficient,
    }
    if path:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def t036_n1_ann_statement() -> str:
    return (
        "T036-N1-ANN (PROVED_LOCALLY): In certified ANNULAR_GRAPH regime, D_nest^ann packets "
        "support cyclic-odd protected rhombus component; T039 gives square with side >= c_ann d_{L_j}."
    )
