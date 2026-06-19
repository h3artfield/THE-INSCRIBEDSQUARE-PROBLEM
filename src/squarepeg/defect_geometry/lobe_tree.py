"""Lobe tree from polygonal defect arc."""

from __future__ import annotations

from dataclasses import dataclass, field

from squarepeg.area_variation.polygonal_arc import PolygonalArc
from squarepeg.area_variation.signed_area import relative_area_increment
from squarepeg.defect_geometry.lobe import LobeRecord

Point = tuple[float, float]


@dataclass
class LobeTree:
    root: LobeRecord
    nodes: dict[str, LobeRecord] = field(default_factory=dict)
    max_depth: int = 0


def _diameter(points: list[Point]) -> float:
    m = 0.0
    for i, p in enumerate(points):
        for q in points[i + 1 :]:
            m = max(m, ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5)
    return max(m, 1e-12)


def build_lobe_tree(points: list[Point], *, max_depth: int = 5, node_id: str = "L0") -> LobeTree:
    """Binary refinement tree; each node is a lobe candidate on a subarc."""
    n = len(points)
    nodes: dict[str, LobeRecord] = {}

    def rec(i0: int, i1: int, depth: int, pid: str | None, nid: str) -> LobeRecord:
        sub = points[i0 : i1 + 1]
        area = relative_area_increment(sub)
        diam = _diameter(sub)
        rec_node = LobeRecord(
            interval=(i0 / max(n - 1, 1), i1 / max(n - 1, 1)),
            arc_vertices=tuple(sub),
            chord=(sub[-1], sub[0]),
            orientation_sign=1 if area >= 0 else -1,
            diameter=diam,
            enclosed_area=abs(area),
            parent_id=pid,
            lobe_id=nid,
        )
        nodes[nid] = rec_node
        if depth < max_depth and i1 - i0 >= 2:
            mid = (i0 + i1) // 2
            c0 = rec(i0, mid, depth + 1, nid, f"{nid}a")
            c1 = rec(mid, i1, depth + 1, nid, f"{nid}b")
            rec_node.children = [c0.lobe_id, c1.lobe_id]
        return rec_node

    root = rec(0, n - 1, 0, None, node_id)
    depth = max((len(k) for k in nodes), default=1)
    return LobeTree(root=root, nodes=nodes, max_depth=depth)


def tree_from_arc(arc: PolygonalArc, **kwargs) -> LobeTree:
    return build_lobe_tree(list(arc.vertices), **kwargs)
