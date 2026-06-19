"""T065PR diffuse permuton residual elimination (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.bounded_depth_order import certify_t077a
from squarepeg.defect_extraction.infinite_gate_measure import gate_set_of_leaf
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.nonsummable_concentration import certify_t076
from squarepeg.defect_extraction.planar_permuton_rigidity import certify_t074r_planar, certify_t077_planar
from squarepeg.defect_extraction.summable_block_geometry import audit_summable_block_geometry
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable
from squarepeg.defect_extraction.t073i_surgery import certify_t073i_v2
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T065PRStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
ResidualRoute = Literal[
    "T073I",
    "T076_CONCENTRATED",
    "T076_FINITE_CENTER",
    "INFINITE_INTRUSION_TREE",
    "UNBOUNDED_BRANCHING_INTRUSION_TREE",
    "INFINITE_CENTER_THICK",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_HULL",
    "POSITIVE_SCALE_NONANNULAR",
    "GENUINELY_DIFFUSE_RESIDUAL",
]


@dataclass
class T065PRCertificate:
    status: T065PRStatus
    route: ResidualRoute
    diffuse_eliminated: bool
    residual_ledger_updated: bool
    messages: list[str]


def _route_from_t077(outcome: str) -> ResidualRoute:
    mapping = {
        "ROUTED_TO_T073I": "T073I",
        "INFINITE_INTRUSION_DEPTH": "INFINITE_INTRUSION_TREE",
        "UNBOUNDED_BRANCHING": "UNBOUNDED_BRANCHING_INTRUSION_TREE",
        "INFINITE_CENTER_PROLIFERATION": "INFINITE_CENTER_THICK",
        "PARAMETER_DISCONNECTED": "PARAMETER_DISCONNECTED",
        "NON_JORDAN_HULL": "NON_JORDAN_HULL",
        "GENUINELY_DIFFUSE_RESIDUAL": "GENUINELY_DIFFUSE_RESIDUAL",
    }
    return mapping.get(outcome, "GENUINELY_DIFFUSE_RESIDUAL")


def certify_t065pr(
    lam: DiffuseNoncrossingWindingLamination,
    leaf: EssentialLeaf,
    param_indices: list[int] | None = None,
    *,
    D: int = 8,
    B: int = 4,
    K: int = 4,
) -> T065PRCertificate:
    """T065PR: finite-intrusion diffuse gate sequence reduction."""
    gs = gate_set_of_leaf(leaf, count=20)
    decomp = extend_decomposition_to_countable(gs, target_blocks=12)
    geom = audit_summable_block_geometry(decomp.blocks, gs)
    t077a = certify_t077a(gs, leaf, D=D, B=B, K=K)
    t077 = certify_t077_planar(gs, leaf, D=D, B=B, K=K)
    t076 = certify_t076(gs)
    t074r = certify_t074r_planar(gs, leaf)
    route: ResidualRoute = "GENUINELY_DIFFUSE_RESIDUAL"
    status: T065PRStatus = "CONJECTURAL_TARGET"
    diffuse_eliminated = False
    if geom.summable:
        t073i = certify_t073i_v2(gs, leaf)
        if t073i.status == "PROVED_LOCALLY":
            route = "T073I"
            status = "PROVED_LOCALLY_PARTIAL"
    elif t076.branch == "CONCENTRATED_ORDER_INTERACTION":
        route = "T076_CONCENTRATED"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t076.branch == "FINITE_CENTER_ORDER_INTERACTION":
        route = "T076_FINITE_CENTER"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t077a.status == "PROVED_LOCALLY" and not t077a.diffuse_limit_possible:
        route = _route_from_t077(t077.outcome)
        status = "PROVED_LOCALLY_PARTIAL"
        diffuse_eliminated = route != "GENUINELY_DIFFUSE_RESIDUAL"
    elif t074r.outcome in ("INFINITE_NESTED_INTRUSION_RAY", "UNBOUNDED_BRANCHING"):
        route = (
            "INFINITE_INTRUSION_TREE"
            if t074r.outcome == "INFINITE_NESTED_INTRUSION_RAY"
            else "UNBOUNDED_BRANCHING_INTRUSION_TREE"
        )
        status = "PROVED_LOCALLY_PARTIAL"
        diffuse_eliminated = True
    elif t077.genuinely_diffuse:
        route = "GENUINELY_DIFFUSE_RESIDUAL"
    return T065PRCertificate(
        status=status,
        route=route,
        diffuse_eliminated=diffuse_eliminated,
        residual_ledger_updated=diffuse_eliminated,
        messages=[f"route={route}, t077a={t077a.status}, t077={t077.outcome}"],
    )
