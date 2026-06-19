"""End density improvement (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class DensityImprovementStep:
    node_id: str
    m_v: float
    phi_v: float
    child_m_sum: float
    child_phi_sum: float
    theta: float
    improvement_holds: bool


@dataclass
class EndDensityImprovementAudit:
    steps: list[DensityImprovementStep]
    strict_improvement: bool
    packing_reverse: bool
    messages: list[str]


def audit_end_density_improvement(tree: CanonicalIntrusionTree) -> EndDensityImprovementAudit:
    steps: list[DensityImprovementStep] = []
    strict = True
    packing = True
    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        rec = cylinder_density(tree, nid)
        child_m = sum(cylinder_density(tree, c).m_v for c in node.child_ids if c in tree.nodes)
        child_phi = sum(cylinder_density(tree, c).phi_v for c in node.child_ids if c in tree.nodes)
        theta = child_m / rec.m_v if rec.m_v > 1e-9 else 1.0
        imp = rec.m_v <= 0.95 * rec.phi_v + child_m if rec.phi_v > 0 else True
        pack = child_phi <= 0.9 * rec.phi_v if rec.phi_v > 0 else True
        if not imp:
            strict = False
        if not pack:
            packing = False
        steps.append(
            DensityImprovementStep(nid, rec.m_v, rec.phi_v, child_m, child_phi, theta, imp)
        )
    return EndDensityImprovementAudit(
        steps=steps,
        strict_improvement=strict,
        packing_reverse=packing,
        messages=[f"steps={len(steps)}, strict={strict}, packing={packing}"],
    )
