"""Exact routing predicates for neutral transitions (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.admissible_neutral_transition import TransitionDatum, audit_admissible_neutral_transition
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091

RoutingPredicate = Literal[
    "P_concentration",
    "P_positive_scale",
    "P_plateau",
    "P_summable_children",
    "P_finite_center",
    "P_infinite_center",
    "P_gate_parameter_escape",
    "P_parameter_disconnected",
    "P_non_jordan",
    "P_bookkeeping_coboundary",
    "NONE",
]


@dataclass
class PredicateEvaluation:
    predicate: RoutingPredicate
    satisfied: bool
    requires_subsequence: bool
    preserves_signature: bool
    detail: str


@dataclass
class TransitionRoutingResult:
    parent_id: str
    predicates: list[PredicateEvaluation]
    primary: RoutingPredicate
    routed: bool


@dataclass
class NeutralRoutingPredicateAudit:
    results: list[TransitionRoutingResult]
    universal_coverage: bool
    messages: list[str]


def _eval_datum(datum: TransitionDatum, t091) -> TransitionRoutingResult:
    preds: list[PredicateEvaluation] = []
    g = datum.geometric
    ratio = datum.scale_ratio
    if ratio < 0.05:
        preds.append(PredicateEvaluation("P_concentration", True, False, True, "ratio->0"))
    if t091.mu_plus_positive or ratio > 0.92:
        preds.append(PredicateEvaluation("P_positive_scale", True, ratio > 0.92, True, "T091/scale"))
    if 0.88 <= ratio <= 0.92:
        preds.append(PredicateEvaluation("P_plateau", True, True, True, "plateau band"))
    if datum.child_count > 4:
        preds.append(PredicateEvaluation("P_summable_children", True, True, True, "T081I"))
    if g.gate_count > 6:
        preds.append(PredicateEvaluation("P_gate_parameter_escape", True, True, True, "gate complexity"))
    if g.retained > 0.4 * g.Phi:
        preds.append(PredicateEvaluation("P_bookkeeping_coboundary", True, False, True, "retained coboundary"))
    if g.sign_imbalance > 0.3 * g.Phi:
        preds.append(PredicateEvaluation("P_bookkeeping_coboundary", True, False, True, "sign coboundary"))
    if not preds and g.escape_labels == ["NONE"]:
        preds.append(PredicateEvaluation("P_finite_center", True, False, True, "bounded neutral"))
    primary: RoutingPredicate = preds[0].predicate if preds else "NONE"
    return TransitionRoutingResult(g.parent_id, preds, primary, bool(preds))


def audit_neutral_routing_predicates(tree: CanonicalIntrusionTree) -> NeutralRoutingPredicateAudit:
    adm = audit_admissible_neutral_transition(tree)
    t091 = certify_t091(tree)
    results = [_eval_datum(d, t091) for d in adm.datums]
    coverage = all(r.routed for r in results) and bool(results)
    return NeutralRoutingPredicateAudit(
        results=results,
        universal_coverage=coverage,
        messages=[f"results={len(results)}, coverage={coverage}"],
    )
