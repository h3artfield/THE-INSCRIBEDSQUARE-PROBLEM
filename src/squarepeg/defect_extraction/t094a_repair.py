"""T094-A repair via equality-core extraction (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.deficit_distribution import audit_deficit_distribution
from squarepeg.defect_extraction.deficit_semicontinuity import audit_deficit_semicontinuity
from squarepeg.defect_extraction.deficit_to_contraction import certify_t095
from squarepeg.defect_extraction.equality_core_compactness import audit_equality_core_compactness
from squarepeg.defect_extraction.equality_compatibility import audit_equality_compatibility
from squarepeg.defect_extraction.tree_core_selection import certify_t096

T094AStatus = Literal["CONJECTURAL_REPAIRED_TARGET", "PROVED_LOCALLY"]
T094AVariant = Literal["T094_A_UNIFORM", "T094_A_ALMOST_EVERYWHERE", "NOT_PROVED"]
T094ARoute = Literal[
    "T095_CONTRACTION",
    "CONCENTRATION",
    "FINITE_CENTER",
    "BAD_RESIDUAL",
    "EQUALITY_CORE_TANGENT",
    "NOT_REPAIRED",
]


@dataclass
class T094ACertificate:
    status: T094AStatus
    variant: T094AVariant
    route: T094ARoute
    simultaneous_equality: bool
    messages: list[str]


def certify_t094a(tree: CanonicalIntrusionTree) -> T094ACertificate:
    t091 = certify_t091(tree)
    if t091.mu_plus_positive:
        return T094ACertificate(
            "PROVED_LOCALLY", "T094_A_UNIFORM", "BAD_RESIDUAL", False, ["T091 route"]
        )
    t095 = certify_t095(tree)
    t096 = certify_t096(tree)
    dist = audit_deficit_distribution(tree)
    compact = audit_equality_core_compactness(tree)
    semi = audit_deficit_semicontinuity()

    if t095.status == "PROVED_LOCALLY" and dist.dominant == "DISTRIBUTED_POSITIVE":
        return T094ACertificate(
            "PROVED_LOCALLY",
            "T094_A_UNIFORM",
            "T095_CONTRACTION",
            False,
            ["deficit implies contraction"],
        )
    if t096.status == "PROVED_LOCALLY" and compact.compactness_holds:
        vanish = all(t.all_deficits_vanish for t in compact.tangents)
        if vanish and semi.all_closed_for_equality:
            return T094ACertificate(
                "PROVED_LOCALLY",
                "T094_A_UNIFORM",
                "EQUALITY_CORE_TANGENT",
                True,
                ["uniform core equality"],
            )
        if vanish:
            return T094ACertificate(
                "CONJECTURAL_REPAIRED_TARGET",
                "T094_A_ALMOST_EVERYWHERE",
                "EQUALITY_CORE_TANGENT",
                False,
                ["semicontinuity gap on RETAINED_SKELETON, SIGN_GROUPING"],
            )
    if t096.core_found and not semi.all_closed_for_equality:
        return T094ACertificate(
            "CONJECTURAL_REPAIRED_TARGET",
            "NOT_PROVED",
            "NOT_REPAIRED",
            False,
            ["core extracted; semicontinuity blocks uniform equality"],
        )
    return T094ACertificate(
        "CONJECTURAL_REPAIRED_TARGET",
        "NOT_PROVED",
        "NOT_REPAIRED",
        False,
        ["T094-A not closed"],
    )


def diagnose_d050_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t094a = certify_t094a(tree)
    t095 = certify_t095(tree)
    t096 = certify_t096(tree)
    semi = audit_deficit_semicontinuity()

    if t094a.status == "PROVED_LOCALLY" and t094a.simultaneous_equality:
        return "A"
    if t095.status == "PROVED_LOCALLY":
        return "B"
    if t094a.variant == "T094_A_ALMOST_EVERYWHERE":
        return "C"
    if not t096.core_found and t095.status != "PROVED_LOCALLY":
        return "E"
    if not semi.all_closed_for_equality or t094a.route == "NOT_REPAIRED":
        return "E"
    return "E"
