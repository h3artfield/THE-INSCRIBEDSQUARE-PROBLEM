"""T072C, T065P nonsummable order reduction (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.countable_order_reduction import certify_t065c
from squarepeg.defect_extraction.infinite_gate_measure import gate_set_of_leaf
from squarepeg.defect_extraction.intrinsic_order_tail import audit_intrinsic_nonsummability
from squarepeg.defect_extraction.intrusion_depth_from_order import certify_t074r_v2
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.nonsummable_concentration import certify_t076
from squarepeg.defect_extraction.permuton_rigidity import certify_t077
from squarepeg.defect_extraction.t073i_surgery import certify_t073i_v2
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T072CStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T065PStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]


@dataclass
class T072CCertificate:
    status: T072CStatus
    outcome: str
    t076_branch: str
    messages: list[str]


@dataclass
class T065PCertificate:
    status: T065PStatus
    outcome: str
    surgery_route: str
    messages: list[str]


def certify_t072c(
    leaf: EssentialLeaf,
    gate_set,
    param_indices: list[int],
) -> T072CCertificate:
    t076 = certify_t076(gate_set)
    t077 = certify_t077(gate_set)
    outcome = "GENUINELY_DIFFUSE_JORDAN_GATE_PERMUTON"
    status: T072CStatus = "CONJECTURAL_TARGET"
    if t076.branch == "CONCENTRATED_ORDER_INTERACTION":
        outcome = "T076_CONCENTRATION"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t076.branch == "FINITE_CENTER_ORDER_INTERACTION":
        outcome = "T076_FINITE_CENTER"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t077.outcome == "INFINITE_INTRUSION_DEPTH":
        outcome = "INFINITE_INTRUSION_DEPTH"
    return T072CCertificate(
        status=status,
        outcome=outcome,
        t076_branch=t076.branch,
        messages=t076.messages,
    )


def certify_t065p(
    lam: DiffuseNoncrossingWindingLamination,
    param_indices: list[int] | None = None,
) -> T065PCertificate:
    t065c = certify_t065c(lam, param_indices)
    outcome = t065c.outcome
    status: T065PStatus = "CONJECTURAL_TARGET"
    route = "EXISTING_SURGERY"
    msgs = list(t065c.messages)
    if lam.leaves:
        leaf = lam.leaves[0]
        gs = gate_set_of_leaf(leaf, count=20)
        intrinsic = audit_intrinsic_nonsummability(gs)
        if intrinsic.nonsummable:
            t076 = certify_t076(gs)
            t077 = certify_t077(gs)
            if t076.status == "PROVED_LOCALLY_CLASSIFIER":
                route = f"T076_{t076.branch}"
                status = "PROVED_LOCALLY_PARTIAL"
                outcome = t076.branch
            elif t077.genuinely_diffuse:
                outcome = "GENUINELY_DIFFUSE_PERMUTON"
                route = "T077_RESIDUAL"
            t074r = certify_t074r_v2(gs, leaf)
            msgs.extend(t074r.messages)
        else:
            t073i = certify_t073i_v2(gs, leaf)
            if t073i.status == "PROVED_LOCALLY":
                route = "T073I"
                outcome = "T073I"
    return T065PCertificate(
        status=status,
        outcome=outcome,
        surgery_route=route,
        messages=msgs,
    )
