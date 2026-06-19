"""Child-center measure nu_v (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.countable_child_order import CountableChildFamily, extract_countable_family
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

ChildCenterClass = Literal[
    "CONCENTRATED",
    "FINITE_CENTER",
    "DIFFUSE",
    "BOUNDARY_SUPPORTED",
    "CANTOR_SUPPORTED",
]


@dataclass
class ChildCenterAtom:
    center: tuple[float, float]
    mass: float
    weight: float


@dataclass
class ChildCenterMeasure:
    parent_id: str
    atoms: list[ChildCenterAtom]
    total_mass: float
    center_class: ChildCenterClass


@dataclass
class ChildCenterAudit:
    measures: list[ChildCenterMeasure]
    primary_class: ChildCenterClass
    routes_t064: bool
    routes_t062: bool
    diffuse_child: bool
    messages: list[str]


def sig_mass(child_defect: float, diameter: float) -> float:
    return child_defect * (1.0 + diameter)


def build_child_center_measure(family: CountableChildFamily) -> ChildCenterMeasure:
    masses = [sig_mass(r.defect, r.diameter) for r in family.children]
    Z = sum(masses) or 1.0
    atoms = [
        ChildCenterAtom(r.center, m, m / Z)
        for r, m in zip(family.children, masses)
    ]
    centers = len({(round(a.center[0], 1), round(a.center[1], 1)) for a in atoms})
    cc: ChildCenterClass = "DIFFUSE"
    if centers == 1:
        cc = "CONCENTRATED"
    elif centers <= 4:
        cc = "FINITE_CENTER"
    elif any(a.center[0] > 0.9 or a.center[0] < 0.1 for a in atoms):
        cc = "BOUNDARY_SUPPORTED"
    elif centers > 8:
        cc = "CANTOR_SUPPORTED"
    return ChildCenterMeasure(family.parent_id, atoms, Z, cc)


def audit_child_center_measures(tree: CanonicalIntrusionTree) -> ChildCenterAudit:
    measures: list[ChildCenterMeasure] = []
    for nid, node in tree.nodes.items():
        if len(node.child_ids) < 3:
            continue
        fam = extract_countable_family(tree, nid)
        if fam:
            measures.append(build_child_center_measure(fam))
    primary: ChildCenterClass = "FINITE_CENTER"
    if measures:
        primary = max(measures, key=lambda m: m.total_mass).center_class
    return ChildCenterAudit(
        measures=measures,
        primary_class=primary,
        routes_t064=primary == "CONCENTRATED",
        routes_t062=primary == "FINITE_CENTER",
        diffuse_child=primary in ("DIFFUSE", "CANTOR_SUPPORTED"),
        messages=[f"primary={primary}, measures={len(measures)}"],
    )
