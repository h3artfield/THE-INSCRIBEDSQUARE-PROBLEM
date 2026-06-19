"""Deficit distribution classification (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.corona_deficit_budget import audit_corona_deficit_budget
from squarepeg.defect_extraction.ledger_deficits import audit_ledger_deficits
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

DeficitClass = Literal[
    "DIFFUSE_SMALL",
    "CONCENTRATED",
    "DISTRIBUTED_POSITIVE",
    "BOUNDARY_DOMINATED",
    "BAD_EXIT_DOMINATED",
]


@dataclass
class DeficitDistributionRecord:
    node_id: str
    deficit_class: DeficitClass
    D_L_over_Phi: float
    concentrated_fraction: float


@dataclass
class DeficitDistributionAudit:
    records: list[DeficitDistributionRecord]
    dominant: DeficitClass
    routes_t095: bool
    messages: list[str]


def audit_deficit_distribution(tree: CanonicalIntrusionTree, *, L: int = 2) -> DeficitDistributionAudit:
    budget = audit_corona_deficit_budget(tree, L=L)
    ld = audit_ledger_deficits(tree)
    records: list[DeficitDistributionRecord] = []
    counts: dict[DeficitClass, int] = {k: 0 for k in (
        "DIFFUSE_SMALL", "CONCENTRATED", "DISTRIBUTED_POSITIVE", "BOUNDARY_DOMINATED", "BAD_EXIT_DOMINATED"
    )}

    for w in budget.windows:
        ratio = w.D_L / w.Phi_v if w.Phi_v > 1e-12 else 0.0
        node_deficits = [d for d in ld.deficits if d.node_id == w.node_id]
        max_d = max((d.delta_k for d in node_deficits), default=0.0)
        total_d = sum(d.delta_k for d in node_deficits) or 1.0
        conc = max_d / total_d
        dc: DeficitClass = "DIFFUSE_SMALL"
        if ratio < 0.05:
            dc = "DIFFUSE_SMALL"
        elif conc > 0.6:
            dc = "CONCENTRATED"
        elif ratio >= 0.08 and conc < 0.4:
            dc = "DISTRIBUTED_POSITIVE"
        elif w.boundary > 0.03 * w.Phi_v:
            dc = "BOUNDARY_DOMINATED"
        elif w.bad > 0.02 * w.Phi_v:
            dc = "BAD_EXIT_DOMINATED"
        counts[dc] += 1
        records.append(DeficitDistributionRecord(w.node_id, dc, ratio, conc))

    dominant = max(counts, key=counts.get)  # type: ignore[arg-type]
    routes = dominant == "DISTRIBUTED_POSITIVE" or dominant == "DIFFUSE_SMALL"
    return DeficitDistributionAudit(
        records=records,
        dominant=dominant,
        routes_t095=routes,
        messages=[f"dominant={dominant}, t095_route={routes}"],
    )
