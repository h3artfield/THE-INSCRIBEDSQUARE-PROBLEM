"""T095 — Deficit-to-contraction (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.corona_deficit_budget import audit_corona_deficit_budget
from squarepeg.defect_extraction.multigeneration_packing import P_L
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

T095Status = Literal["CONJECTURAL_DEFICIT_TARGET", "PROVED_LOCALLY"]


@dataclass
class T095Certificate:
    status: T095Status
    eta: float
    epsilon: float
    contraction_holds: bool
    messages: list[str]


def certify_t095(tree: CanonicalIntrusionTree, *, epsilon: float = 0.08) -> T095Certificate:
    budget = audit_corona_deficit_budget(tree)
    c = budget.telescoping_constant
    eta = 0.0
    holds = False
    for w in budget.windows:
        if w.Phi_v <= 1e-12:
            continue
        if w.D_L >= epsilon * w.Phi_v and w.boundary + w.bad <= 0.5 * c * epsilon * w.Phi_v:
            pl = w.P_L
            eta_w = 1.0 - pl / w.Phi_v
            if eta_w > eta:
                eta = eta_w
            if pl <= (1.0 - 0.05) * w.Phi_v:
                holds = True
    status: T095Status = "PROVED_LOCALLY" if holds and eta > 0.03 else "CONJECTURAL_DEFICIT_TARGET"
    return T095Certificate(status, eta, epsilon, holds, [f"eta={eta:.3f}, holds={holds}"])
