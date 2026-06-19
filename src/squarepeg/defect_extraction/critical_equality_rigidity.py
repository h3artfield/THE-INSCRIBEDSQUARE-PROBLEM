"""T094 — Critical equality rigidity (Directive 048)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.equality_model_classifier import audit_equality_model_classifier
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.self_similar_end_models import audit_self_similar_end_models

T094Status = Literal["CONJECTURAL_RIGIDITY_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T094Route = Literal[
    "T087_CARLESON",
    "T090R_FROSTMAN",
    "CONCENTRATION",
    "FINITE_CENTER",
    "ANNULAR_THIN",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN",
    "CRITICAL_MODEL_REMAINS",
]


@dataclass
class T094Certificate:
    status: T094Status
    route: T094Route
    critical_model_found: bool
    messages: list[str]


def certify_t094(tree: CanonicalIntrusionTree) -> T094Certificate:
    eq = audit_equality_model_classifier(tree)
    carl = audit_end_signature_carleson(tree)
    inc = audit_incidence_concentration(tree)
    t091 = certify_t091(tree)
    models = audit_self_similar_end_models()

    if carl.satisfies_carleson:
        return T094Certificate("PROVED_LOCALLY_CLASSIFIER", "T087_CARLESON", False, ["Carleson"])
    if inc.concentration_class == "CONCENTRATED":
        return T094Certificate("PROVED_LOCALLY_CLASSIFIER", "CONCENTRATION", False, ["concentrated"])
    if inc.concentration_class == "FINITE_CENTER":
        return T094Certificate("PROVED_LOCALLY_CLASSIFIER", "FINITE_CENTER", False, ["finite-center"])
    if t091.mu_plus_positive:
        return T094Certificate("PROVED_LOCALLY_CLASSIFIER", "ANNULAR_THIN", False, ["positive-scale"])
    if "PARALLEL_THIN_MODEL" in eq.models_found:
        return T094Certificate("PROVED_LOCALLY_CLASSIFIER", "ANNULAR_THIN", False, ["thin model"])
    if models.result == "SELF_SIMILAR_CRITICAL_COUNTERMODEL":
        return T094Certificate(
            "CONJECTURAL_RIGIDITY_TARGET",
            "CRITICAL_MODEL_REMAINS",
            True,
            ["countermodel in self-similar audit"],
        )
    if not carl.satisfies_carleson and "DISJOINT_SELF_SIMILAR_PACKING" in eq.models_found:
        return T094Certificate(
            "CONJECTURAL_RIGIDITY_TARGET",
            "CRITICAL_MODEL_REMAINS",
            False,
            ["equality packing without Carleson closure"],
        )
    return T094Certificate(
        "PROVED_LOCALLY_CLASSIFIER",
        "T087_CARLESON" if carl.satisfies_carleson else "FINITE_CENTER",
        False,
        ["default route"],
    )
