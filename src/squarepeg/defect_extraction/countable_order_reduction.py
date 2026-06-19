"""T065C, T072S countable order reduction (Directive 037)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, gate_set_of_leaf
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_countable_blocks import certify_t075
from squarepeg.defect_extraction.nonsummable_block_residual import audit_nonsummable_tail
from squarepeg.defect_extraction.positive_inversion_reduction import certify_t065o
from squarepeg.defect_extraction.summable_block_geometry import audit_summable_block_geometry
from squarepeg.defect_extraction.t073i_surgery import certify_t073i_v2
from squarepeg.defect_extraction.unbounded_width_geometry import certify_t074r
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T065CStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T072SStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class T072SCertificate:
    status: T072SStatus
    summable_components: bool
    t073i_eligible: bool
    messages: list[str]


@dataclass
class T065CCertificate:
    status: T065CStatus
    outcome: str
    t073i_status: str
    messages: list[str]


def certify_t072s(
    leaf: EssentialLeaf,
    gate_set: InfiniteGateSet,
    param_indices: list[int],
) -> T072SCertificate:
    """T072S: summable parameter-component reduction."""
    t075 = certify_t075(gate_set)
    geom = audit_summable_block_geometry(t075.decomposition.blocks, gate_set)
    t073i = certify_t073i_v2(gate_set, leaf)
    status: T072SStatus = "CONJECTURAL_TARGET"
    if geom.summable and t073i.status == "PROVED_LOCALLY":
        status = "PROVED_LOCALLY"
    return T072SCertificate(
        status=status,
        summable_components=geom.summable,
        t073i_eligible=t073i.status == "PROVED_LOCALLY",
        messages=geom.messages,
    )


def certify_t065c(
    lam: DiffuseNoncrossingWindingLamination,
    param_indices: list[int] | None = None,
) -> T065CCertificate:
    """T065C: countable-order diffuse reduction."""
    t065o = certify_t065o(lam, param_indices)
    outcome = t065o.outcome
    status: T065CStatus = "CONJECTURAL_TARGET"
    t073i_status = "CONJECTURAL_TARGET"
    msgs = list(t065o.messages)
    if lam.leaves:
        leaf = lam.leaves[0]
        gs = gate_set_of_leaf(leaf, count=16)
        t073i = certify_t073i_v2(gs, leaf)
        t073i_status = t073i.status
        if t073i.status == "PROVED_LOCALLY":
            outcome = "T073I"
            status = "PROVED_LOCALLY_PARTIAL"
            msgs.extend(t073i.messages)
        else:
            nons = audit_nonsummable_tail(gs)
            if nons.is_nonsummable:
                outcome = "NONSUMMABLE_BLOCK"
            else:
                t074r = certify_t074r(gs)
                if t074r.width_unbounded:
                    outcome = "UNBOUNDED_WIDTH"
    return T065CCertificate(
        status=status,
        outcome=outcome,
        t073i_status=t073i_status,
        messages=msgs,
    )
