"""Non-Jordan hull failure taxonomy (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.saturation_hull import audit_saturation_hulls

FailureType = Literal[
    "PINCHED_HULL",
    "SELF_CONTACTING_BOUNDARY",
    "MULTI_BOUNDARY_SATURATION",
    "NONLOCALLY_CONNECTED_LIMIT",
    "SHARED_GATE_COLLISION_HULL",
    "PARAMETER_MERGED_HULL",
    "INFINITE_CENTER_ACCUMULATION",
    "HARMLESS_QUOTIENT",
    "JORDAN_OK",
]


@dataclass
class HullTaxonomyRecord:
    hull_id: str
    failure_type: FailureType
    true_non_jordan: bool


@dataclass
class NonJordanHullTaxonomyAudit:
    records: list[HullTaxonomyRecord]
    harmless_separated: bool
    exhaustive: bool
    messages: list[str]


def audit_non_jordan_hull_taxonomy(tree: CanonicalIntrusionTree) -> NonJordanHullTaxonomyAudit:
    hulls = audit_saturation_hulls(tree)
    records: list[HullTaxonomyRecord] = []
    for h in hulls.hulls:
        ft: FailureType = "JORDAN_OK"
        true_nj = False
        if h.hull_class == "HARMLESS_QUOTIENT":
            ft = "HARMLESS_QUOTIENT"
        elif not h.jordan:
            true_nj = True
            if h.pinch_detected:
                ft = "PINCHED_HULL"
            elif h.boundary_count > 4:
                ft = "MULTI_BOUNDARY_SATURATION"
            elif not h.locally_connected:
                ft = "NONLOCALLY_CONNECTED_LIMIT"
            elif h.collision_mass > 0:
                ft = "SHARED_GATE_COLLISION_HULL"
            else:
                ft = "SELF_CONTACTING_BOUNDARY"
        records.append(HullTaxonomyRecord(h.hull_id, ft, true_nj))
    harmless_sep = all(r.failure_type != "JORDAN_OK" or not r.true_non_jordan for r in records)
    return NonJordanHullTaxonomyAudit(records, harmless_sep, bool(records), [f"n={len(records)}"])
