"""T071R, T065O positive-inversion reduction (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.countable_order_blocks import certify_t073i
from squarepeg.defect_extraction.finite_width_gate_surgery import certify_t073, certify_t073_lamination
from squarepeg.defect_extraction.gate_inversion_energy import inversion_energy
from squarepeg.defect_extraction.gate_permuton import audit_gate_permuton
from squarepeg.defect_extraction.infinite_gate_lamination_surgery import certify_t068i
from squarepeg.defect_extraction.infinite_gate_measure import gate_set_of_leaf
from squarepeg.defect_extraction.infinite_gate_reduction import certify_t065i
from squarepeg.defect_extraction.monotone_gate_width import audit_monotone_width, WidthClass
from squarepeg.defect_extraction.noncrossing_order_width import certify_t074
from squarepeg.defect_extraction.parameter_component_order import certify_t072r
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T071RStatus = Literal["CONJECTURAL_REFINEMENT", "PROVED_LOCALLY_CLASSIFIER"]
T065OStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]

T071ROutcome = Literal[
    "FINITE_MONOTONE_WIDTH",
    "COUNTABLE_SUMMABLE_BLOCKS",
    "UNBOUNDED_WIDTH_T074",
    "DISCONNECTED_CONCENTRATION",
    "DIFFUSE_PERMUTON",
    "NON_JORDAN",
]

T065OOutcome = Literal[
    "T066", "T068", "T069", "T068I", "T073", "T073I",
    "INTRUSION_TREE", "NON_JORDAN", "DISCONNECTED", "DIFFUSE_PERMUTON", "INFINITE_CENTER",
]


@dataclass
class T071RCertificate:
    status: T071RStatus
    outcome: T071ROutcome
    inversion_energy: float
    width_class: WidthClass
    messages: list[str]


@dataclass
class T065OCertificate:
    status: T065OStatus
    outcome: T065OOutcome
    t073_status: str
    messages: list[str]


def certify_t071r(gate_set, *, K: int = 4) -> T071RCertificate:
    inv = inversion_energy(gate_set)
    width = audit_monotone_width(gate_set, K=K)
    t074 = certify_t074(gate_set, K=K)
    outcome: T071ROutcome = "DIFFUSE_PERMUTON"
    status: T071RStatus = "CONJECTURAL_REFINEMENT"
    if inv.energy < 0.01:
        outcome = "FINITE_MONOTONE_WIDTH"
    elif width.width_class == "FINITE_ORDER_WIDTH" and width.asymptotic_width is not None:
        t073 = certify_t073(gate_set, _dummy_leaf(gate_set.leaf_id), K=K)
        if t073.status == "PROVED_LOCALLY":
            outcome = "FINITE_MONOTONE_WIDTH"
            status = "PROVED_LOCALLY_CLASSIFIER"
    elif width.width_class == "COUNTABLE_SUMMABLE_WIDTH":
        outcome = "COUNTABLE_SUMMABLE_BLOCKS"
    elif t074.unbounded_width:
        outcome = "UNBOUNDED_WIDTH_T074"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif inv.positive_class:
        perm = audit_gate_permuton(gate_set)
        outcome = "DIFFUSE_PERMUTON"
    return T071RCertificate(
        status=status,
        outcome=outcome,
        inversion_energy=inv.energy,
        width_class=width.width_class,
        messages=[f"inv={inv.energy:.4f}, width={width.width_class}"],
    )


def certify_t065o(
    lam: DiffuseNoncrossingWindingLamination,
    param_indices: list[int] | None = None,
    *,
    K: int = 4,
) -> T065OCertificate:
    t065i = certify_t065i(lam, param_indices, gate_order_assumed=False, K=K)
    t073 = certify_t073_lamination(lam, K=K)
    outcome: T065OOutcome = "DIFFUSE_PERMUTON"
    status: T065OStatus = "CONJECTURAL_TARGET"
    msgs = list(t065i.messages)
    if t065i.outcome == "T066":
        outcome = "T066"
    elif t065i.outcome == "T068":
        outcome = "T068"
    elif t065i.outcome == "T069":
        outcome = "T069"
    elif t065i.outcome == "T068I":
        outcome = "T068I"
    elif t073.status == "PROVED_LOCALLY":
        outcome = "T073"
        status = "PROVED_LOCALLY_PARTIAL"
        msgs.extend(t073.messages)
    elif t065i.outcome == "INFINITE_CENTER":
        outcome = "INFINITE_CENTER"
    elif t065i.outcome == "PARAMETER_DISCONNECTED":
        outcome = "DISCONNECTED"
    elif t065i.outcome == "POSITIVE_INVERSION":
        gs = gate_set_of_leaf(lam.leaves[0], count=16) if lam.leaves else None
        if gs:
            t073i = certify_t073i(gs)
            if t073i.status == "PROVED_LOCALLY":
                outcome = "T073I"
                status = "PROVED_LOCALLY_PARTIAL"
            else:
                t071r = certify_t071r(gs, K=K)
                if t071r.outcome == "UNBOUNDED_WIDTH_T074":
                    outcome = "INTRUSION_TREE"
    return T065OCertificate(
        status=status,
        outcome=outcome,
        t073_status=t073.status,
        messages=msgs,
    )


def _dummy_leaf(leaf_id: str):
    from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

    return EssentialLeaf(
        leaf_id, 1, ((0, 0), (1, 0), (1, 1), (0, 1)), 1.0, 1.414, 0.5, None, []
    )
