"""T068, T065S, diffuse lamination reduction (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.compatible_lamination_ears import audit_ear_compatibility
from squarepeg.defect_extraction.finite_gate_lamination import audit_finite_gate_lamination, extract_jordan_sublamination
from squarepeg.defect_extraction.measurable_ear_selection import audit_measurable_ear_selection
from squarepeg.defect_extraction.multigate_lamination_signature import signature_bound_uniform
from squarepeg.defect_extraction.multigate_leaf_exhaustion import truncate_by_transverse_mass
from squarepeg.defect_extraction.ordered_leaf_surgery import certify_t066, is_ordered_two_gate_lamination
from squarepeg.defect_extraction.thick_leaf_band import classify_t067r
from squarepeg.defect_extraction.thin_lamination_signature import certify_t069
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T068Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]
T065SStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T065SOutcome = Literal[
    "T066_ORDERED_TWO_GATE",
    "T068_FINITE_MULTIGATE",
    "T069_THIN_ECCENTRIC",
    "ANNULAR_BAND_SQUARE",
    "INFINITE_GATE_JORDAN",
    "NON_JORDAN",
    "POSITIVE_INVERSION",
    "PARAMETER_DISCONNECTED",
    "MULTICENTER_THICK",
]


@dataclass
class T068Certificate:
    status: T068Status
    uniform_M: int | None
    measurable_selection: bool
    gate_ordered: bool
    tail_vanishing: bool
    signature_uniform: bool
    messages: list[str]


@dataclass
class T065SCertificate:
    status: T065SStatus
    outcome: T065SOutcome
    t068: T068Certificate | None
    finite_dense_eliminated: bool
    messages: list[str]


def certify_t068(
    lam: DiffuseNoncrossingWindingLamination,
    *,
    M: int = 6,
    inversion_density: float = 0.0,
) -> T068Certificate:
    """T068: finite-multigate Jordan lamination surgery."""
    if is_ordered_two_gate_lamination(lam):
        return T068Certificate(
            status="PROVED_LOCALLY",
            uniform_M=2,
            measurable_selection=True,
            gate_ordered=True,
            tail_vanishing=True,
            signature_uniform=True,
            messages=["Degenerates to T066 ordered two-gate"],
        )
    sub = extract_jordan_sublamination(lam)
    fg = audit_finite_gate_lamination(lam, M=M)
    leaves = sub.jordan_leaves or lam.leaves
    pairs = list(zip(fg.leaf_gate_data, leaves[: len(fg.leaf_gate_data)]))
    if fg.gate_class == "INFINITE_GATE_RESIDUAL":
        return T068Certificate(
            status="CONJECTURAL_TARGET",
            uniform_M=None,
            measurable_selection=False,
            gate_ordered=False,
            tail_vanishing=False,
            signature_uniform=False,
            messages=["INFINITE_GATE_JORDAN_LAMINATION residual"],
        )
    sel = audit_measurable_ear_selection(pairs)
    compat = audit_ear_compatibility(sel.selections, lam.leaves, inversion_density=inversion_density)
    exhaust = truncate_by_transverse_mass(sel.selections, lam.leaves)
    sig = signature_bound_uniform(exhaust, M=M or 6)
    status: T068Status = "CONJECTURAL_TARGET"
    if (
        fg.gate_class == "FINITE_GATE_M"
        and sel.measurable
        and compat.lamination_gate_ordered
        and exhaust.tail_tends_zero
        and sig.uniform_in_leaves
        and len(sel.selections) >= 1
    ):
        status = "PROVED_LOCALLY"
    msgs = fg.messages + sel.messages + compat.messages + exhaust.messages
    return T068Certificate(
        status=status,
        uniform_M=fg.uniform_M,
        measurable_selection=sel.measurable,
        gate_ordered=compat.lamination_gate_ordered,
        tail_vanishing=exhaust.tail_tends_zero,
        signature_uniform=sig.uniform_in_leaves,
        messages=msgs,
    )


def certify_t065s(
    lam: DiffuseNoncrossingWindingLamination,
    *,
    M: int = 6,
    inversion_density: float = 0.0,
) -> T065SCertificate:
    """T065S: diffuse lamination surgery reduction."""
    t066 = certify_t066(lam)
    t068 = certify_t068(lam, M=M, inversion_density=inversion_density)
    t069 = certify_t069(lam.leaves)
    outcome: T065SOutcome = "MULTICENTER_THICK"
    status: T065SStatus = "CONJECTURAL_TARGET"
    msgs: list[str] = []
    if t066.status == "PROVED_LOCALLY" and t066.is_ordered_two_gate:
        outcome = "T066_ORDERED_TWO_GATE"
        status = "PROVED_LOCALLY_PARTIAL"
        msgs.append("T066 branch")
    elif t068.status == "PROVED_LOCALLY":
        outcome = "T068_FINITE_MULTIGATE"
        status = "PROVED_LOCALLY_PARTIAL"
        msgs.extend(t068.messages)
    elif t069.status == "PROVED_LOCALLY":
        outcome = "T069_THIN_ECCENTRIC"
        status = "PROVED_LOCALLY_PARTIAL"
        msgs.extend(t069.messages)
    elif inversion_density > 0.1:
        outcome = "POSITIVE_INVERSION"
        msgs.append("POSITIVE_INVERSION_GATE_LAMINATION")
    elif t068.uniform_M is None and t068.measurable_selection is False:
        outcome = "INFINITE_GATE_JORDAN"
        msgs.append("INFINITE_GATE_JORDAN_LAMINATION")
    else:
        t067r = classify_t067r(
            t066_closed=t066.status == "PROVED_LOCALLY",
            t068_closed=t068.status == "PROVED_LOCALLY",
            t069_closed=t069.status == "PROVED_LOCALLY",
            outer=lam.leaves[0] if lam.leaves else None,
            inner=lam.leaves[1] if len(lam.leaves) > 1 else None,
        )
        if t067r.outcome == "THICK_NESTED_BAND":
            outcome = "ANNULAR_BAND_SQUARE"
        msgs.extend(t067r.messages)
    eliminated = outcome in ("T066_ORDERED_TWO_GATE", "T068_FINITE_MULTIGATE", "T069_THIN_ECCENTRIC", "ANNULAR_BAND_SQUARE")
    return T065SCertificate(
        status=status,
        outcome=outcome,
        t068=t068,
        finite_dense_eliminated=eliminated,
        messages=msgs,
    )
