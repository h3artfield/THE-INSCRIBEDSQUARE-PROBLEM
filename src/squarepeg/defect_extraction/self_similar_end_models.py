"""Self-similar end model audit (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode
from squarepeg.defect_extraction.cantor_end_surgery import build_middle_thirds_cantor_tree
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density, cylinder_density
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

ModelAuditResult = Literal[
    "SELF_SIMILAR_MODELS_CARLESON",
    "SELF_SIMILAR_CRITICAL_COUNTERMODEL",
    "MODEL_DEPENDENT",
]


@dataclass
class SelfSimilarModelRecord:
    name: str
    mu_root: float
    r_root: float
    phi_root: float
    D_root: float
    carleson: bool
    singleton_fraction: float
    non_carleson: bool


@dataclass
class SelfSimilarEndModelsAudit:
    models: list[SelfSimilarModelRecord]
    result: ModelAuditResult
    countermodel_name: str | None
    messages: list[str]


def build_binary_equal_ratio_cantor(*, levels: int = 4, ratio: float = 0.58) -> CanonicalIntrusionTree:
    """Binary equal-ratio Cantor with co-located centers (singleton shrinking ends)."""
    nodes: dict[str, IntrusionTreeNode] = {}
    root_id = "root"
    nodes[root_id] = IntrusionTreeNode(
        node_id=root_id,
        param_interval=(0.0, 1.0),
        diameter=1.0,
        defect=0.2,
        gate_count=4,
        center=(0.5, 0.5),
        sign=1,
        parent_id=None,
        child_ids=[],
        jordan_hull=True,
    )

    def add(level: int, lo: float, hi: float, parent: str, r: float, idx: int) -> None:
        if level >= levels:
            nid = f"L{level}_{idx}"
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(lo, hi),
                diameter=r,
                defect=0.18 * r,
                gate_count=2,
                center=(0.5, 0.5),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            return
        mid = (lo + hi) / 2
        for j, (a, b) in enumerate([(lo, mid), (mid, hi)]):
            nid = f"L{level}_{idx}_{j}"
            nr = r * ratio
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(a, b),
                diameter=nr,
                defect=0.15 * r,
                gate_count=2,
                center=(0.5, 0.5),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            add(level + 1, a, b, nid, nr, idx * 2 + j)

    add(0, 0.0, 1.0, root_id, 0.55, 0)
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=levels,
    )


def build_moran_cantor_tree(*, levels: int = 4, ratios: tuple[float, float] = (0.55, 0.62)) -> CanonicalIntrusionTree:
    """Unequal-ratio Moran Cantor with singleton centers."""
    nodes: dict[str, IntrusionTreeNode] = {}
    root_id = "root"
    nodes[root_id] = IntrusionTreeNode(
        node_id=root_id,
        param_interval=(0.0, 1.0),
        diameter=1.0,
        defect=0.22,
        gate_count=4,
        center=(0.5, 0.5),
        sign=1,
        parent_id=None,
        child_ids=[],
        jordan_hull=True,
    )

    def add(level: int, lo: float, hi: float, parent: str, r: float, idx: int) -> None:
        if level >= levels:
            nid = f"M{level}_{idx}"
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(lo, hi),
                diameter=r,
                defect=0.2 * r,
                gate_count=2,
                center=(0.5, 0.5),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            return
        mid = (lo + hi) / 2
        for j, (a, b) in enumerate([(lo, mid), (mid, hi)]):
            ratio = ratios[j % 2]
            nid = f"M{level}_{idx}_{j}"
            nr = r * ratio
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(a, b),
                diameter=nr,
                defect=0.17 * r,
                gate_count=2,
                center=(0.5, 0.5),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            add(level + 1, a, b, nid, nr, idx * 2 + j)

    add(0, 0.0, 1.0, root_id, 0.55, 0)
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=levels,
    )


def build_rotating_center_tree(*, levels: int = 4, ratio: float = 0.58) -> CanonicalIntrusionTree:
    """Rotating-center binary tree — tests finite-center vs infinite-center."""
    nodes: dict[str, IntrusionTreeNode] = {}
    root_id = "root"
    nodes[root_id] = IntrusionTreeNode(
        node_id=root_id,
        param_interval=(0.0, 1.0),
        diameter=1.0,
        defect=0.2,
        gate_count=4,
        center=(0.5, 0.5),
        sign=1,
        parent_id=None,
        child_ids=[],
        jordan_hull=True,
    )

    def add(level: int, lo: float, hi: float, parent: str, r: float, idx: int) -> None:
        if level >= levels:
            angle = idx * 0.7
            cx = 0.5 + 0.08 * r * (idx % 5 - 2)
            cy = 0.5 + 0.08 * r * ((idx + 1) % 5 - 2)
            nid = f"R{level}_{idx}"
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(lo, hi),
                diameter=r,
                defect=0.18 * r,
                gate_count=2,
                center=(cx, cy),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            return
        mid = (lo + hi) / 2
        for j, (a, b) in enumerate([(lo, mid), (mid, hi)]):
            nid = f"R{level}_{idx}_{j}"
            nr = r * ratio
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(a, b),
                diameter=nr,
                defect=0.15 * r,
                gate_count=2,
                center=(0.5, 0.5),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            add(level + 1, a, b, nid, nr, idx * 2 + j)

    add(0, 0.0, 1.0, root_id, 0.55, 0)
    return CanonicalIntrusionTree(
        root_id=root_id,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=levels,
    )


def _audit_model(name: str, tree: CanonicalIntrusionTree) -> SelfSimilarModelRecord:
    root = cylinder_density(tree, tree.root_id)
    carl = audit_end_signature_carleson(tree)
    nc = audit_noncarleson_end_density(tree)
    split = audit_singleton_continuum_split(tree)
    return SelfSimilarModelRecord(
        name=name,
        mu_root=root.m_v,
        r_root=tree.nodes[tree.root_id].diameter,
        phi_root=root.phi_v,
        D_root=root.D_v,
        carleson=carl.satisfies_carleson,
        singleton_fraction=split.E0_fraction,
        non_carleson=nc.intrinsically_non_carleson,
    )


def audit_self_similar_end_models() -> SelfSimilarEndModelsAudit:
    models = [
        _audit_model("binary_equal_ratio", build_binary_equal_ratio_cantor()),
        _audit_model("moran_unequal", build_moran_cantor_tree()),
        _audit_model("middle_thirds", build_middle_thirds_cantor_tree(levels=4)),
        _audit_model("rotating_center", build_rotating_center_tree()),
    ]
    carleson_count = sum(1 for m in models if m.carleson)
    critical = [
        m
        for m in models
        if m.non_carleson and m.singleton_fraction > 0.9 and not m.carleson
    ]
    result: ModelAuditResult = "MODEL_DEPENDENT"
    counter: str | None = None
    if carleson_count == len(models):
        result = "SELF_SIMILAR_MODELS_CARLESON"
    elif critical:
        result = "SELF_SIMILAR_CRITICAL_COUNTERMODEL"
        counter = critical[0].name

    return SelfSimilarEndModelsAudit(
        models=models,
        result=result,
        countermodel_name=counter,
        messages=[f"result={result}, counter={counter}"],
    )
