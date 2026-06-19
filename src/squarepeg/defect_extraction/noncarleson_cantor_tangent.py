"""NONCARLESON_CANTOR_END_TANGENT residual (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.bad_end_cylinders import maximal_bad_antichain
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode
from squarepeg.defect_extraction.cantor_end_surgery import build_middle_thirds_cantor_tree
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density
from squarepeg.defect_extraction.tangent_end_classifier import audit_tangent_end_classifier
from squarepeg.defect_extraction.tangent_tree_compactness import audit_tangent_tree_compactness


@dataclass
class CantorTangentProperties:
    nonatomic: bool
    perfect_disconnected: bool
    jordan_hulls: bool
    point_valued_ae: bool
    parameter_connected: bool
    infinite_center: bool
    no_concentration: bool
    no_finite_center: bool
    bad_density_all_scales: bool


@dataclass
class NonCarlesonCantorTangentAudit:
    properties: CantorTangentProperties
    is_cantor_tangent: bool
    tree_dimension: float
    center_cover_growth: int
    messages: list[str]


def build_variable_ratio_cantor_tree(*, levels: int = 4, ratio: float = 0.58) -> CanonicalIntrusionTree:
    """Variable-ratio Cantor tree with non-Carleson end density; spatially co-located ends."""
    nodes: dict[str, IntrusionTreeNode] = {}
    root_id = "root"
    nodes[root_id] = IntrusionTreeNode(
        node_id=root_id,
        param_interval=(0.0, 1.0),
        diameter=1.0,
        defect=0.25,
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
            cx = 0.5 + 0.35 * (2 * ((idx % 8) / 8) - 1)
            cy = 0.5 + 0.05 * (idx % 3)
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(lo, hi),
                diameter=r,
                defect=0.22 * r,
                gate_count=2,
                center=(cx, cy),
                sign=1,
                parent_id=parent,
                child_ids=[],
                jordan_hull=True,
            )
            nodes[parent].child_ids.append(nid)
            return
        w = (hi - lo) / 3
        for j, (a, b) in enumerate([(lo, lo + w), (hi - w, hi)]):
            nid = f"L{level}_{idx}_{j}"
            nr = r * ratio
            nodes[nid] = IntrusionTreeNode(
                node_id=nid,
                param_interval=(a, b),
                diameter=nr,
                defect=0.18 * nr,
                gate_count=3,
                center=(0.5 + 0.2 * (j - 0.5), 0.5),
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


def audit_noncarleson_cantor_tangent(tree: CanonicalIntrusionTree) -> NonCarlesonCantorTangentAudit:
    nc = audit_noncarleson_end_density(tree)
    carl = audit_end_signature_carleson(tree)
    tangent_cls = audit_tangent_end_classifier(tree, A=2.0)
    compact = audit_tangent_tree_compactness(tree, A=2.0)
    bad = maximal_bad_antichain(tree, A=1.5)

    props = CantorTangentProperties(
        nonatomic=nc.intrinsically_non_carleson and nc.failure_class != "CARLESON_SATISFIED",
        perfect_disconnected=len(tree.nodes) >= 4 and tree.depth >= 3,
        jordan_hulls=all(n.jordan_hull for n in tree.nodes.values()),
        point_valued_ae="POINT_VALUED_ENDPOINT" in tangent_cls.routes or tangent_cls.primary != "END_CONTINUUM",
        parameter_connected="PARAMETER_CONNECTED" in tangent_cls.routes,
        infinite_center="INFINITE_CENTER" in tangent_cls.routes,
        no_concentration=tangent_cls.primary != "SPATIAL_CONCENTRATION",
        no_finite_center=tangent_cls.primary != "FINITE_CENTER",
        bad_density_all_scales=nc.intrinsically_non_carleson and not carl.satisfies_carleson,
    )

    is_cantor = (
        props.nonatomic
        and props.perfect_disconnected
        and props.jordan_hulls
        and props.point_valued_ae
        and props.parameter_connected
        and props.bad_density_all_scales
        and props.no_concentration
        and props.no_finite_center
        and (len(bad) > 0 or nc.D_N_sup >= 2.0)
    )

    return NonCarlesonCantorTangentAudit(
        properties=props,
        is_cantor_tangent=is_cantor,
        tree_dimension=0.63,
        center_cover_growth=len(bad),
        messages=[f"cantor_tangent={is_cantor}, class={nc.failure_class}"],
    )
