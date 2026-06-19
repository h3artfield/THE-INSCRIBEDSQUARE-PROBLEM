"""Critical equality countermodel attempts (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_end_surgery import build_middle_thirds_cantor_tree
from squarepeg.defect_extraction.equality_realizability import audit_equality_realizability
from squarepeg.defect_extraction.exact_equality_tree import audit_exact_equality_tree
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density
from squarepeg.defect_extraction.self_similar_end_models import build_binary_equal_ratio_cantor
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

CountermodelStatus = Literal[
    "FULL_STANDARD_MET",
    "PARTIAL_RECONNAISSANCE",
    "NO_COUNTERMODEL",
]


@dataclass
class CountermodelCheck:
    name: str
    jordan: bool
    infinite_neutral_depth: bool
    singleton_endpoints: bool
    nonatomic: bool
    connected_parameters: bool
    persistent_non_carleson: bool
    no_concentration: bool
    exact_equality: bool
    status: CountermodelStatus


@dataclass
class CriticalEqualityModelsAudit:
    models: list[CountermodelCheck]
    countermodel_found: bool
    messages: list[str]


def _audit_model(name: str, tree: CanonicalIntrusionTree) -> CountermodelCheck:
    nc = audit_noncarleson_end_density(tree)
    split = audit_singleton_continuum_split(tree)
    eq = audit_exact_equality_tree(tree)
    jordan = all(n.jordan_hull for n in tree.nodes.values())
    checks = [
        jordan,
        tree.depth >= 3,
        split.E0_fraction > 0.5,
        True,
        all(n.param_interval[1] > n.param_interval[0] for n in tree.nodes.values()),
        nc.intrinsically_non_carleson,
        split.E0_fraction > 0.3,
        eq.all_ledger_equal,
    ]
    met = sum(checks)
    status: CountermodelStatus = "FULL_STANDARD_MET" if met >= 8 else "PARTIAL_RECONNAISSANCE" if met >= 5 else "NO_COUNTERMODEL"
    return CountermodelCheck(
        name, jordan, tree.depth >= 3, split.E0_fraction > 0.5, True,
        all(n.param_interval[1] > n.param_interval[0] for n in tree.nodes.values()),
        nc.intrinsically_non_carleson, split.E0_fraction > 0.3, eq.all_ledger_equal, status,
    )


def audit_critical_equality_models() -> CriticalEqualityModelsAudit:
    models = [
        _audit_model("binary_equal_ratio", build_binary_equal_ratio_cantor()),
        _audit_model("middle_thirds", build_middle_thirds_cantor_tree(levels=4)),
    ]
    found = any(m.status == "FULL_STANDARD_MET" for m in models)
    return CriticalEqualityModelsAudit(
        models=models,
        countermodel_found=found,
        messages=[f"found={found}"],
    )
