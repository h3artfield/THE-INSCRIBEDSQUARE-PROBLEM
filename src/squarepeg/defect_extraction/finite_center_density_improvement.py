"""Finite-center density improvement (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_signature_packing import audit_child_signature_packing
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

ImprovementRoute = Literal[
    "CONCENTRATED_CHILD_GROUP",
    "FINITE_CENTER_T062",
    "PARAMETER_DISCONNECTED",
    "HULL_DEGENERATION",
    "STRICT_DENSITY_DECAY",
    "CARLESON_DENSITY_GAIN",
    "NO_IMPROVEMENT",
]


@dataclass
class CenterGroupRecord:
    node_id: str
    group_count: int
    max_child_D: float
    parent_D: float
    epsilon_gain: float
    route: ImprovementRoute


@dataclass
class FiniteCenterDensityImprovementAudit:
    groups: list[CenterGroupRecord]
    K_bound: int
    uniform_epsilon: float
    any_improvement: bool
    messages: list[str]


def _center_groups(tree: CanonicalIntrusionTree, node_id: str, *, K: int = 4) -> int:
    node = tree.nodes[node_id]
    if not node.child_ids:
        return 1
    buckets: dict[tuple[int, int], float] = {}
    for cid in node.child_ids:
        if cid not in tree.nodes:
            continue
        c = tree.nodes[cid].center
        key = (round(c[0] * K), round(c[1] * K))
        buckets[key] = buckets.get(key, 0.0) + cylinder_density(tree, cid).m_v
    return len(buckets)


def audit_finite_center_density_improvement(
    tree: CanonicalIntrusionTree,
    *,
    K: int = 4,
) -> FiniteCenterDensityImprovementAudit:
    packing = audit_child_signature_packing(tree)
    inc = audit_incidence_concentration(tree)
    groups: list[CenterGroupRecord] = []
    epsilons: list[float] = []
    improved = False

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        parent = cylinder_density(tree, nid)
        child_D = [cylinder_density(tree, c).D_v for c in node.child_ids if c in tree.nodes]
        max_D = max(child_D, default=0.0)
        gc = _center_groups(tree, nid, K=K)
        route: ImprovementRoute = "NO_IMPROVEMENT"
        eps = 0.0

        if inc.concentration_class == "CONCENTRATED":
            route = "CONCENTRATED_CHILD_GROUP"
            eps = 0.1
            improved = True
        elif inc.concentration_class == "FINITE_CENTER":
            route = "FINITE_CENTER_T062"
            eps = 0.08
            improved = True
        elif gc > K:
            route = "HULL_DEGENERATION"
            eps = 0.05
        elif max_D <= (1.0 - 0.05) * parent.D_v + 0.01 and parent.D_v > 0:
            route = "STRICT_DENSITY_DECAY"
            eps = 0.05
            improved = True
        elif packing.status in ("STRICT_CONTRACTION", "GEOMETRICALLY_DERIVED"):
            route = "CARLESON_DENSITY_GAIN"
            eps = 1.0 - packing.uniform_theta
            improved = eps > 0.02
        elif any(not tree.nodes[c].jordan_hull for c in node.child_ids if c in tree.nodes):
            route = "HULL_DEGENERATION"

        epsilons.append(eps)
        groups.append(CenterGroupRecord(nid, gc, max_D, parent.D_v, eps, route))

    uniform_eps = max(epsilons, default=0.0)
    return FiniteCenterDensityImprovementAudit(
        groups=groups,
        K_bound=K,
        uniform_epsilon=uniform_eps,
        any_improvement=improved,
        messages=[f"K={K}, improved={improved}, eps={uniform_eps:.3f}"],
    )
