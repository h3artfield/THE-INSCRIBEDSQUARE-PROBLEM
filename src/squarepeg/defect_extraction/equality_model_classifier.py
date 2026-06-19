"""Equality model classifier (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_corona import audit_cantor_corona
from squarepeg.defect_extraction.signature_excess import audit_signature_excess

EqualityModel = Literal[
    "ONE_CHILD_CHAIN",
    "DISJOINT_SELF_SIMILAR_PACKING",
    "ANNULAR_EQUALITY_MODEL",
    "PARALLEL_THIN_MODEL",
    "SIGN_CANCELLATION_MODEL",
    "DEGENERATE_SHARED_GATE_MODEL",
    "UNKNOWN_EQUALITY_MODEL",
]


@dataclass
class EqualityModelRecord:
    node_id: str
    model: EqualityModel
    jordan_realizable: bool
    exact_equality: bool


@dataclass
class EqualityModelClassifierAudit:
    records: list[EqualityModelRecord]
    models_found: list[EqualityModel]
    messages: list[str]


def audit_equality_model_classifier(tree: CanonicalIntrusionTree) -> EqualityModelClassifierAudit:
    corona = audit_cantor_corona(tree)
    excess = audit_signature_excess(tree)
    records: list[EqualityModelRecord] = []
    found: set[EqualityModel] = set()

    for er in excess.records:
        node = tree.nodes[er.node_id]
        exact = abs(er.P_v - er.Phi_v) < 0.05 * max(er.Phi_v, 1e-9)
        model: EqualityModel = "UNKNOWN_EQUALITY_MODEL"
        if len(node.child_ids) == 1:
            model = "ONE_CHILD_CHAIN"
        elif "SIGN_CANCELLATION_EXCESS" in er.mechanisms:
            model = "SIGN_CANCELLATION_MODEL"
        elif "THIN_CHILD_EXCESS" in er.mechanisms:
            model = "PARALLEL_THIN_MODEL"
        elif "SHARED_GATE_EXCESS" in er.mechanisms:
            model = "DEGENERATE_SHARED_GATE_MODEL"
        elif exact and len(node.child_ids) == 2:
            model = "DISJOINT_SELF_SIMILAR_PACKING"
        elif "CENTER_DRIFT_EXCESS" in er.mechanisms:
            model = "ANNULAR_EQUALITY_MODEL"
        if exact or any(c.node_id == er.node_id and c.node_class == "NEUTRAL" for c in corona.classifications):
            found.add(model)
        records.append(
            EqualityModelRecord(er.node_id, model, node.jordan_hull, exact)
        )

    return EqualityModelClassifierAudit(
        records=records,
        models_found=sorted(found),
        messages=[f"models={list(found)}"],
    )
