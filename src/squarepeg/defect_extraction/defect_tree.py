"""Defect tree classification (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.packet_shape_audit import ShapeClass

NodeBranch = Literal["ORDERED_SURGERY_FOREST", "PROTECTED_GEOMETRY", "UNRESOLVED_RESIDUAL"]


@dataclass
class DefectTreeNode:
    node_id: str
    interval: tuple[float, float]
    defect_mass: float
    sign: int
    shape_class: ShapeClass
    gate_ordered: bool
    branch: NodeBranch
    children: list[str] = field(default_factory=list)


@dataclass
class DefectTree:
    nodes: list[DefectTreeNode]
    unresolved_count: int


def classify_node(
    *,
    node_id: str,
    interval: tuple[float, float],
    defect_mass: float,
    sign: int,
    shape_class: ShapeClass,
    clean: bool,
    gate_ordered: bool,
) -> DefectTreeNode:
    if clean and gate_ordered:
        branch: NodeBranch = "ORDERED_SURGERY_FOREST"
    elif shape_class == "ECCENTRIC_PACKET" or not clean:
        branch = "UNRESOLVED_RESIDUAL"
    else:
        branch = "PROTECTED_GEOMETRY"
    return DefectTreeNode(
        node_id=node_id,
        interval=interval,
        defect_mass=defect_mass,
        sign=sign,
        shape_class=shape_class,
        gate_ordered=gate_ordered,
        branch=branch,
    )
