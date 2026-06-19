"""End density martingale audit (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_density_process import audit_end_density_process
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

MartingaleClass = Literal[
    "MARTINGALE",
    "SUBMARTINGALE",
    "SUPERMARTINGALE",
    "NONE",
]


@dataclass
class MartingaleDefect:
    parent_id: str
    child_id: str
    D_parent: float
    D_child: float
    mass_defect: float
    phi_defect: float


@dataclass
class EndDensityMartingaleAudit:
    classification: MartingaleClass
    defects: list[MartingaleDefect]
    cross_child_interaction: bool
    retained_skeleton: bool
    phi_nonadditive: bool
    messages: list[str]


def audit_end_density_martingale(tree: CanonicalIntrusionTree) -> EndDensityMartingaleAudit:
    proc = audit_end_density_process(tree)
    defects: list[MartingaleDefect] = []
    sub_ok = True
    super_ok = True
    mart_ok = True
    cross = False
    retained = False
    phi_bad = not proc.additive_mass

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        parent = cylinder_density(tree, nid)
        for cid in node.child_ids:
            if cid not in tree.nodes:
                continue
            child = cylinder_density(tree, cid)
            m_def = child.m_v - parent.m_v / max(len(node.child_ids), 1)
            p_def = child.phi_v - parent.phi_v / max(len(node.child_ids), 1)
            defects.append(
                MartingaleDefect(nid, cid, parent.D_v, child.D_v, m_def, p_def)
            )
            if child.D_v > parent.D_v * 1.02:
                sub_ok = False
            if child.D_v < parent.D_v * 0.98:
                super_ok = False
            if abs(child.D_v - parent.D_v) > 0.05 * max(parent.D_v, 1e-9):
                mart_ok = False
            if abs(m_def) > 0.01 * max(parent.m_v, 1e-9):
                cross = True

    children_mass = sum(
        sum(cylinder_density(tree, c).m_v for c in node.child_ids if c in tree.nodes)
        for nid, node in tree.nodes.items()
        if node.child_ids
    )
    root_m = cylinder_density(tree, tree.root_id).m_v
    if children_mass > root_m * 0.5:
        retained = True

    if mart_ok and proc.additive_mass:
        cls: MartingaleClass = "MARTINGALE"
    elif sub_ok:
        cls = "SUBMARTINGALE"
    elif super_ok:
        cls = "SUPERMARTINGALE"
    else:
        cls = "NONE"

    return EndDensityMartingaleAudit(
        classification=cls,
        defects=defects[:20],
        cross_child_interaction=cross,
        retained_skeleton=retained,
        phi_nonadditive=phi_bad,
        messages=[f"class={cls}, cross={cross}, phi_nonadd={phi_bad}"],
    )
