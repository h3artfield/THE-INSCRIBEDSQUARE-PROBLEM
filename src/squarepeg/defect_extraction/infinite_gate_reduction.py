"""T065I, T071 infinite-gate reduction (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.diffuse_lamination_reduction import certify_t065s, certify_t068
from squarepeg.defect_extraction.gate_inversion_energy import certify_t070, inversion_energy
from squarepeg.defect_extraction.infinite_gate_lamination_surgery import certify_t068i
from squarepeg.defect_extraction.infinite_gate_measure import gate_set_of_leaf
from squarepeg.defect_extraction.multicenter_thick_leaf import audit_multicenter_thick
from squarepeg.defect_extraction.ordered_leaf_surgery import certify_t066
from squarepeg.defect_extraction.parameter_support_components import certify_t072
from squarepeg.defect_extraction.thin_lamination_signature import certify_t069
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T065IStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T065IOutcome = Literal[
    "T066",
    "T068",
    "T069",
    "T068I",
    "FINITE_CENTER_THICK",
    "POSITIVE_INVERSION",
    "PARAMETER_DISCONNECTED",
    "INFINITE_CENTER",
    "NON_JORDAN",
]
T071Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]


@dataclass
class T071Certificate:
    status: T071Status
    outcome: Literal[
        "T064D_DISCONNECTED",
        "T062_FINITE_CENTER",
        "INFINITE_INTRUSION_TREE",
        "DIFFUSE_POSITIVE_INVERSION",
        "NON_JORDAN_LIMIT",
    ]
    inversion_density: float
    messages: list[str]


@dataclass
class T065ICertificate:
    status: T065IStatus
    outcome: T065IOutcome
    t068i_status: str
    finite_dense_eliminated: bool
    messages: list[str]


def certify_t071(gate_set, *, iota_0: float = 0.05) -> T071Certificate:
    inv = inversion_energy(gate_set)
    outcome: Literal[
        "T064D_DISCONNECTED",
        "T062_FINITE_CENTER",
        "INFINITE_INTRUSION_TREE",
        "DIFFUSE_POSITIVE_INVERSION",
        "NON_JORDAN_LIMIT",
    ] = "DIFFUSE_POSITIVE_INVERSION"
    status: T071Status = "CONJECTURAL_STRUCTURAL_TARGET"
    if inv.energy < iota_0:
        outcome = "T064D_DISCONNECTED"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif inv.energy >= iota_0:
        outcome = "DIFFUSE_POSITIVE_INVERSION"
    return T071Certificate(
        status=status,
        outcome=outcome,
        inversion_density=inv.energy,
        messages=[f"inversion={inv.energy:.4f}"],
    )


def certify_t065i(
    lam: DiffuseNoncrossingWindingLamination,
    param_indices: list[int] | None = None,
    *,
    gate_order_assumed: bool = False,
    K: int = 4,
) -> T065ICertificate:
    """T065I: infinite-gate diffuse lamination reduction."""
    t065s = certify_t065s(lam)
    t068i = certify_t068i(lam, gate_order_assumed=gate_order_assumed)
    outcome: T065IOutcome = "NON_JORDAN"
    status: T065IStatus = "CONJECTURAL_TARGET"
    msgs = list(t065s.messages)
    if t065s.outcome == "T066_ORDERED_TWO_GATE":
        outcome = "T066"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t065s.outcome == "T068_FINITE_MULTIGATE":
        outcome = "T068"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t065s.outcome == "T069_THIN_ECCENTRIC":
        outcome = "T069"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t068i.status in ("PROVED_LOCALLY", "PROVED_LOCALLY_GATE_ORDERED"):
        outcome = "T068I"
        status = "PROVED_LOCALLY_PARTIAL"
        msgs.extend(t068i.messages)
    else:
        for leaf in lam.leaves:
            gs = gate_set_of_leaf(leaf, count=24)
            inv = inversion_energy(gs)
            if inv.positive_class:
                outcome = "POSITIVE_INVERSION"
                msgs.append("POSITIVE_INVERSION_GATE_LAMINATION")
                break
            if param_indices is not None:
                t072 = certify_t072(leaf, param_indices, K=K)
                if t072.outcome == "FINITE_CONNECTED_BLOCKS":
                    outcome = "FINITE_CENTER_THICK"
                    status = "PROVED_LOCALLY_PARTIAL"
                elif t072.outcome in ("DISCONNECTED_CONCENTRATION", "INFINITE_INTRUSION_TREE"):
                    outcome = "PARAMETER_DISCONNECTED"
            mc = audit_multicenter_thick(leaf, K=K)
            if mc.center_class in ("INFINITE_CENTER_THICK", "MULTICENTER_THICK_WINDING_LAMINATION"):
                outcome = "INFINITE_CENTER"
                msgs.append(mc.center_class)
    eliminated = outcome in ("T066", "T068", "T069", "T068I", "FINITE_CENTER_THICK")
    return T065ICertificate(
        status=status,
        outcome=outcome,
        t068i_status=t068i.status,
        finite_dense_eliminated=eliminated,
        messages=msgs,
    )
