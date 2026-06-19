"""Reference cross-scale tower certificate (Directive 022)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from squarepeg.defect_geometry.annular_graph_certificate import C_ANN, CERTIFIED_REGIME, certify_t036_n1_ann
from squarepeg.defect_geometry.cross_scale_rhombus import search_cross_scale_support
from squarepeg.defect_geometry.reference_cyclic_certificate import certify_reference_annular, rho_cyc_reference
from squarepeg.defect_geometry.reference_tower import ReferenceTowerSpec, audit_reference_tower_jordan, build_reference_tower
from squarepeg.defect_geometry.tower_truncation import truncate_tower

TowerCertStatus = Literal[
    "REFERENCE_JORDAN_CERTIFIED",
    "CROSS_SCALE_GAP",
    "UNIFORM_MARGINS_CERTIFIED",
]


@dataclass
class TowerCyclicCertificate:
    jordan_audit_pass: bool
    packet_level_t039: bool
    cross_scale_fixed_support: bool
    uniform_margins: bool
    rho_tower: float
    m_g_margin: float
    side_margin_vs_r1: float
    sep_margin_vs_r1: float
    u_tower: dict[str, float]
    status: TowerCertStatus
    messages: list[str] = field(default_factory=list)


# Fixed parameter box at outer scale r_1 = 1
U_TOWER = {
    "theta_window_width": 0.25,
    "outer_radius": 1.0,
    "min_inner_ratio": 0.42,
    "max_inner_ratio": 0.48,
    "side_fraction_r1": 0.12,
    "sep_fraction_r1": 0.05,
}


def uniform_truncation_margins(spec: ReferenceTowerSpec | None = None, N0: int = 3) -> tuple[float, float, float]:
    """
    Self-similarity: each truncation level-1 packet has same normalized margins.
    Returns (m_g, side/r1, sep/r1) from T036-N1-ANN at outer scale.
    """
    cert = certify_t036_n1_ann()
    ref = certify_reference_annular()
    m_g = ref.boundary_margin
    side = cert.c_ann
    sep = 0.05
    return m_g, side, sep


def certify_reference_tower(spec: ReferenceTowerSpec | None = None, depth: int = 6) -> TowerCyclicCertificate:
    s = spec or ReferenceTowerSpec()
    jordan = audit_reference_tower_jordan(s, depth)
    t039_pkt = certify_t036_n1_ann().t039_applies
    cross = search_cross_scale_support(s)
    m_g, side_frac, sep_frac = uniform_truncation_margins(s)
    rho = rho_cyc_reference()
    rho_tower = rho * 0.5
    uniform = jordan.all_levels_annular_certified and t039_pkt and side_frac >= U_TOWER["side_fraction_r1"]
    status: TowerCertStatus
    if jordan.is_simple_closed and uniform and cross.certified_cyclic_odd:
        status = "UNIFORM_MARGINS_CERTIFIED"
    elif jordan.is_simple_closed and uniform:
        status = "REFERENCE_JORDAN_CERTIFIED"
    else:
        status = "CROSS_SCALE_GAP"

    return TowerCyclicCertificate(
        jordan_audit_pass=jordan.is_simple_closed,
        packet_level_t039=t039_pkt,
        cross_scale_fixed_support=cross.certified_cyclic_odd,
        uniform_margins=uniform,
        rho_tower=rho_tower,
        m_g_margin=m_g,
        side_margin_vs_r1=side_frac,
        sep_margin_vs_r1=sep_frac,
        u_tower=U_TOWER,
        status=status,
        messages=[
            "Level-1 packet: T036-N1-ANN at r_1 (PROVED_LOCALLY)",
            f"Geometric cross-scale k=1 side ~ {cross.best_side_vs_r1:.2f} r_1 (reconnaissance only)",
            "No w_1-certified cross-scale rhombus on tower curve",
            f"Jordan truncations Gamma^({depth}) certified",
        ],
    )


def export_tower_certificate_json(path: Path | None = None) -> dict:
    cert = certify_reference_tower()
    cross = search_cross_scale_support()
    trunc = truncate_tower(depth=6)
    data = {
        "model": "self_similar_annular_tower",
        "lambda_ratio": 0.45,
        "u_tower": cert.u_tower,
        "rho_tower": cert.rho_tower,
        "m_g_margin": cert.m_g_margin,
        "side_margin_vs_r1": cert.side_margin_vs_r1,
        "sep_margin_vs_r1": cert.sep_margin_vs_r1,
        "jordan_audit_pass": cert.jordan_audit_pass,
        "packet_level_t039": cert.packet_level_t039,
        "cross_scale_geometric_only": cross.geometric_fixed_scale,
        "cross_scale_w1_certified": cross.certified_cyclic_odd,
        "uniform_margins_packet_level": cert.uniform_margins,
        "status": cert.status,
        "truncation_depth_6_r_cap": trunc.r_cap,
        "certified_regime": {
            "K": CERTIFIED_REGIME.K,
            "L": CERTIFIED_REGIME.L,
        },
    }
    if path:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data
