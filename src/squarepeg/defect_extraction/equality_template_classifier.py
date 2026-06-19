"""Equality template classifier (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.exact_equality_tree import audit_exact_equality_tree
from squarepeg.defect_extraction.signature_excess import audit_signature_excess

EqualityTemplate = Literal[
    "DOMINANT_RAY_EQUALITY",
    "ANNULAR_EQUALITY",
    "THIN_PARALLEL_EQUALITY",
    "SHARED_GATE_DEGENERACY",
    "SIGN_CANCELLATION_EQUALITY",
    "FINITE_CENTER_SELF_SIMILARITY",
    "INFINITE_CENTER_EQUALITY",
    "DISJOINT_SELF_SIMILAR_PACKING",
    "NO_JORDAN_REALIZABLE_EQUALITY",
    "NOT_EQUALITY",
]


@dataclass
class TemplateRecord:
    node_id: str
    template: EqualityTemplate
    defining_equations: list[str]


@dataclass
class EqualityTemplateClassifierAudit:
    records: list[TemplateRecord]
    templates_found: list[EqualityTemplate]
    exhaustive: bool
    messages: list[str]


def audit_equality_template_classifier(tree: CanonicalIntrusionTree) -> EqualityTemplateClassifierAudit:
    eq_tree = audit_exact_equality_tree(tree)
    excess = audit_signature_excess(tree)
    records: list[TemplateRecord] = []
    found: set[EqualityTemplate] = set()

    for er in excess.records:
        exact = abs(er.P_v - er.Phi_v) < 0.05 * max(er.Phi_v, 1e-9)
        tmpl: EqualityTemplate = "NOT_EQUALITY"
        eqs: list[str] = []
        if not exact:
            tmpl = "NOT_EQUALITY"
        elif len(tree.nodes[er.node_id].child_ids) == 1:
            tmpl = "DOMINANT_RAY_EQUALITY"
            eqs = ["P(v)=Phi(w)", "single child"]
        elif "SIGN_CANCELLATION_EXCESS" in er.mechanisms:
            tmpl = "SIGN_CANCELLATION_EQUALITY"
            eqs = ["sum signed wedge = 0"]
        elif "SHARED_GATE_EXCESS" in er.mechanisms:
            tmpl = "SHARED_GATE_DEGENERACY"
            eqs = ["crosscut = gate chord"]
        elif "THIN_CHILD_EXCESS" in er.mechanisms:
            tmpl = "THIN_PARALLEL_EQUALITY"
            eqs = ["diam(child)/diam(parent) → 0"]
        elif "CENTER_DRIFT_EXCESS" in er.mechanisms:
            tmpl = "ANNULAR_EQUALITY"
            eqs = ["centers on annulus"]
        elif len(tree.nodes[er.node_id].child_ids) == 2:
            tmpl = "DISJOINT_SELF_SIMILAR_PACKING"
            eqs = ["Phi(w1)+Phi(w2)=Phi(v)", "disjoint hulls"]
        else:
            tmpl = "FINITE_CENTER_SELF_SIMILARITY"
            eqs = ["P=Phi", "finite branches"]
        if exact:
            found.add(tmpl)
        records.append(TemplateRecord(er.node_id, tmpl, eqs))

    return EqualityTemplateClassifierAudit(
        records=records,
        templates_found=sorted(found),
        exhaustive=eq_tree.tree_class != "COUNTABLE_CHILD_EQUAL",
        messages=[f"templates={list(found)}, exhaustive={eq_tree.tree_class != 'COUNTABLE_CHILD_EQUAL'}"],
    )
