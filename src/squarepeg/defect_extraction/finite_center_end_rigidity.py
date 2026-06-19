"""T089 — Finite-center non-Carleson end rigidity (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.normalized_end_tangent import NormalizedEndTangent
from squarepeg.defect_extraction.tangent_end_classifier import classify_tangent

T089Status = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T089Certificate:
    status: T089Status
    rigidity_holds: bool
    contradicts_bad_tangent: bool
    messages: list[str]


def audit_finite_center_rigidity(
    tangent: NormalizedEndTangent,
    *,
    tree_for_renorm,
) -> T089Certificate:
    """Bad finite-center Jordan tangent must renormalize to Carleson — contradiction if bad."""
    from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

    cls = classify_tangent(tangent)
    finite = cls.primary == "FINITE_CENTER"
    jordan = all(n.jordan_hull for n in tangent.nodes)
    point = "POINT_VALUED_ENDPOINT" in cls.routes
    param_conn = "PARAMETER_CONNECTED" in cls.routes
    concentrated = cls.primary == "SPATIAL_CONCENTRATION"
    atomic = "ATOMIC_RAY" in cls.routes

    if not (finite and jordan and point and param_conn and not concentrated and not atomic):
        return T089Certificate(
            status="CONJECTURAL_CORE_TARGET",
            rigidity_holds=False,
            contradicts_bad_tangent=False,
            messages=["hypotheses not met"],
        )

    carl = audit_end_signature_carleson(tree_for_renorm)
    rigidity = carl.satisfies_carleson
    return T089Certificate(
        status="PROVED_LOCALLY" if rigidity else "CONJECTURAL_CORE_TARGET",
        rigidity_holds=rigidity,
        contradicts_bad_tangent=not rigidity,
        messages=[f"rigidity={rigidity}, carleson={carl.satisfies_carleson}"],
    )


def certify_t089(tree, tangent: NormalizedEndTangent) -> T089Certificate:
    return audit_finite_center_rigidity(tangent, tree_for_renorm=tree)
