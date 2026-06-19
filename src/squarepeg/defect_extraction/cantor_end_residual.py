"""Cantor end residual definition (Directive 043)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_tree_ends import build_end_measure
from squarepeg.defect_extraction.tree_end_signature_measure import audit_tree_end_signature_measure


@dataclass
class CantorEndProperties:
    end_measure_nonatomic: bool
    endpoint_map_cantor: bool
    gate_accumulation: bool
    center_complexity_diverges: bool
    signature_tail_persistent: bool


@dataclass
class CantorEndResidualAudit:
    properties: CantorEndProperties
    is_cantor_residual: bool
    center_count: int
    gate_density: float
    tail_mass: float
    messages: list[str]


def build_binary_diffuse_end_tree(*, depth: int = 5) -> CanonicalIntrusionTree:
    """Binary tree with Bernoulli-like diffuse end measure proxy."""
    from squarepeg.defect_extraction.canonical_intrusion_tree import IntrusionTreeNode

    nodes: dict[str, IntrusionTreeNode] = {}

    def add(level: int, idx: int, parent: str | None, r: float) -> str:
        nid = f"B{level}_{idx}"
        angle = 2 * 3.14159 * idx / (2 ** level + 1)
        cx = 0.5 + 0.25 * (idx % 2) * (1 if level % 2 == 0 else -1)
        cy = 0.5 + 0.1 * level
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(idx / (2 ** level + 1), (idx + 1) / (2 ** level + 1)),
            diameter=r,
            defect=0.04 * r * r * (1 + 0.1 * (idx % 3)),
            gate_count=2 + (idx % 2),
            center=(cx, cy),
            sign=1 if idx % 2 == 0 else -1,
            parent_id=parent,
            child_ids=[],
            jordan_hull=True,
        )
        if parent:
            nodes[parent].child_ids.append(nid)
        if level < depth:
            add(level + 1, 2 * idx, nid, r * 0.55)
            add(level + 1, 2 * idx + 1, nid, r * 0.55)
        return nid

    root = add(0, 0, None, 1.0)
    return CanonicalIntrusionTree(
        root_id=root,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=depth,
    )


def audit_cantor_end_residual(tree: CanonicalIntrusionTree) -> CantorEndResidualAudit:
    """Explicit Cantor end residual via end measure, endpoint map, gate accumulation."""
    em = build_end_measure(tree)
    end_audit = audit_tree_end_signature_measure(tree)
    ends = em.ends
    centers = len({(round(e.spatial_point[0], 1), round(e.spatial_point[1], 1)) for e in ends if e.spatial_point})
    gate_density = sum(
        1 for e in ends if e.gate_order_type != "TWO_GATE"
    ) / max(len(ends), 1)
    tail_mass = 1.0 - end_audit.leaf_end_mass if end_audit.leaf_end_mass < 1.0 else 0.0

    props = CantorEndProperties(
        end_measure_nonatomic=em.measure_class in ("DIFFUSE_CANTOR", "INFINITE_CENTERS"),
        endpoint_map_cantor=end_audit.spatial_class == "CANTOR_END_MEASURE",
        gate_accumulation=gate_density > 0.3,
        center_complexity_diverges=centers > 8,
        signature_tail_persistent=tail_mass > 0.05,
    )
    is_cantor = (
        props.end_measure_nonatomic
        and (props.endpoint_map_cantor or props.center_complexity_diverges)
        and props.signature_tail_persistent
    )
    return CantorEndResidualAudit(
        properties=props,
        is_cantor_residual=is_cantor,
        center_count=centers,
        gate_density=gate_density,
        tail_mass=tail_mass,
        messages=[f"cantor={is_cantor}, centers={centers}, tail={tail_mass:.3f}"],
    )
