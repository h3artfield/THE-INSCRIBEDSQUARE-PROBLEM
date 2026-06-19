"""Defect lobe tree from chord-lobe decomposition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.area_variation.signed_area import relative_area_increment

Point = tuple[float, float]


@dataclass
class LobeNode:
    interval: tuple[float, float]
    signed_area: float
    diameter: float
    winding_sign: int
    depth: int
    children: list["LobeNode"] = field(default_factory=list)


@dataclass
class DefectLobeTree:
    root: LobeNode
    max_depth: int
    max_branching: int
    same_sign_chain_length: int


def build_lobe_tree(
    points: list[Point],
    *,
    max_depth: int = 4,
) -> DefectLobeTree:
    """Binary subdivision lobe tree from polygonal arc."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")

    def make_node(i0: int, i1: int, depth: int) -> LobeNode:
        sub = points[i0 : i1 + 1]
        area = relative_area_increment(sub)
        xs = [p[0] for p in sub]
        ys = [p[1] for p in sub]
        diam = max(max(xs) - min(xs), max(ys) - min(ys), 1e-12)
        node = LobeNode(
            interval=(i0 / n, i1 / n),
            signed_area=area,
            diameter=diam,
            winding_sign=1 if area >= 0 else -1,
            depth=depth,
        )
        if depth < max_depth and i1 - i0 >= 2:
            mid = (i0 + i1) // 2
            node.children = [
                make_node(i0, mid, depth + 1),
                make_node(mid, i1, depth + 1),
            ]
        return node

    root = make_node(0, n - 1, 0)
    max_d = 0
    max_b = 0

    def walk(node: LobeNode) -> None:
        nonlocal max_d, max_b
        max_d = max(max_d, node.depth)
        max_b = max(max_b, len(node.children))
        for c in node.children:
            walk(c)

    walk(root)
    chain = _same_sign_chain(root)
    return DefectLobeTree(root=root, max_depth=max_d, max_branching=max_b, same_sign_chain_length=chain)


def _same_sign_chain(node: LobeNode) -> int:
    best = 1
    for c in node.children:
        if c.winding_sign == node.winding_sign:
            best = max(best, 1 + _same_sign_chain(c))
    return best


def unbounded_area_forces_combinatorics(tree: DefectLobeTree) -> bool:
    """Heuristic: large |area| in unit diameter => depth or branching grows."""
    return (
        tree.max_depth >= 2
        or tree.max_branching >= 2
        or tree.same_sign_chain_length >= 2
        or abs(tree.root.signed_area) > 0.01
    )
