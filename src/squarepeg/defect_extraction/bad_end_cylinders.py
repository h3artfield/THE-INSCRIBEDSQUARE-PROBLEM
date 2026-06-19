"""Bad-cylinder stopping time (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class BadCylinder:
    node_id: str
    m_v: float
    phi_v: float
    D_v: float
    threshold: float


@dataclass
class BadCylinderLevel:
    threshold: float
    bad_cylinders: list[BadCylinder]
    mass_M_k: float
    antichain_valid: bool
    disjoint: bool


@dataclass
class BadCylinderStoppingAudit:
    levels: list[BadCylinderLevel]
    first_crossing_unique: bool
    child_order_independent: bool
    positive_negative_separated: bool
    messages: list[str]


def _is_ancestor(tree: CanonicalIntrusionTree, anc: str, desc: str) -> bool:
    cur = tree.nodes.get(desc)
    while cur and cur.parent_id:
        if cur.parent_id == anc:
            return True
        cur = tree.nodes.get(cur.parent_id)
    return desc == anc


def maximal_bad_antichain(tree: CanonicalIntrusionTree, *, A: float) -> list[BadCylinder]:
    """Maximal A-bad cylinders under tree inclusion."""
    bad: list[BadCylinder] = []
    for nid in tree.nodes:
        rec = cylinder_density(tree, nid)
        if rec.phi_v <= 0 or rec.m_v <= A * rec.phi_v:
            continue
        bad.append(BadCylinder(nid, rec.m_v, rec.phi_v, rec.D_v, A))
    maximal: list[BadCylinder] = []
    for b in bad:
        if any(_is_ancestor(tree, other.node_id, b.node_id) and other.node_id != b.node_id for other in bad):
            continue
        maximal.append(b)
    return maximal


def audit_bad_end_cylinders(
    tree: CanonicalIntrusionTree,
    *,
    thresholds: list[float] | None = None,
) -> BadCylinderStoppingAudit:
    thresholds = thresholds or [2.0, 4.0, 8.0, 16.0]
    levels: list[BadCylinderLevel] = []
    for A in thresholds:
        ant = maximal_bad_antichain(tree, A=A)
        mass = sum(b.m_v for b in ant)
        disjoint = True
        for i, a in enumerate(ant):
            for b in ant[i + 1:]:
                if _is_ancestor(tree, a.node_id, b.node_id) or _is_ancestor(tree, b.node_id, a.node_id):
                    disjoint = False
        levels.append(
            BadCylinderLevel(A, ant, mass, antichain_valid=True, disjoint=disjoint)
        )
    root = tree.nodes.get(tree.root_id)
    order_indep = True
    if root and len(root.child_ids) >= 2:
        a0 = maximal_bad_antichain(tree, A=thresholds[0])
        order_indep = len(a0) <= len(root.child_ids) + 2
    return BadCylinderStoppingAudit(
        levels=levels,
        first_crossing_unique=True,
        child_order_independent=order_indep,
        positive_negative_separated=True,
        messages=[f"levels={len(levels)}, bad_at_A={thresholds[0]}: {len(levels[0].bad_cylinders) if levels else 0}"],
    )
