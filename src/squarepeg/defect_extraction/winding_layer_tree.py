"""Winding-layer component tree (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass, field

from squarepeg.defect_extraction.winding_layers import WindingLayer, build_winding_layers


@dataclass
class LayerTreeNode:
    level: int
    component_id: str
    area: float
    diameter: float
    children: list[str] = field(default_factory=list)
    parent: str | None = None


@dataclass
class WindingLayerTree:
    nodes: list[LayerTreeNode]
    depth: int
    nested: bool


def build_layer_tree(layers: list[WindingLayer]) -> WindingLayerTree:
    """E_{n,k+1} subset E_{n,k}; child at k+1 contained in parent at k."""
    nodes: list[LayerTreeNode] = []
    id_by_level: dict[int, str] = {}
    for layer in layers:
        for comp in layer.components:
            parent = id_by_level.get(layer.level - 1)
            node = LayerTreeNode(
                level=layer.level,
                component_id=comp.component_id,
                area=comp.area,
                diameter=comp.diameter,
                parent=parent,
            )
            if parent:
                for n in nodes:
                    if n.component_id == parent:
                        n.children.append(comp.component_id)
            nodes.append(node)
            id_by_level[layer.level] = comp.component_id
    depth = max((n.level for n in nodes), default=0)
    nested = all(
        nodes[i].area <= nodes[i - 1].area for i in range(1, len(nodes)) if nodes[i].level > nodes[i - 1].level
    ) if len(nodes) > 1 else True
    return WindingLayerTree(nodes=nodes, depth=depth, nested=nested)


def verify_nesting(layers: list[WindingLayer]) -> bool:
    """Higher level components have area <= lower level (nested)."""
    for i in range(len(layers) - 1):
        if layers[i + 1].total_area > layers[i].total_area + 1e-9:
            return False
    return True
