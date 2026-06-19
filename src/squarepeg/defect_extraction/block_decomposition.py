"""Block decomposition of gate graphs (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass, field

from squarepeg.defect_extraction.gate_graph import GateGraph


@dataclass
class BiconnectedBlock:
    block_id: str
    vertices: list[str]
    edges: list[str]
    is_leaf: bool
    is_bridge: bool


@dataclass
class BlockDecomposition:
    blocks: list[BiconnectedBlock]
    cut_vertices: list[str]
    bridges: list[tuple[str, str]]
    leaf_blocks: list[BiconnectedBlock]


def _neighbors(g: GateGraph, vid: str) -> list[str]:
    nbrs: list[str] = []
    for e in g.edges:
        if e.u == vid:
            nbrs.append(e.v)
        elif e.v == vid:
            nbrs.append(e.u)
    return nbrs


def _find_bridges(g: GateGraph) -> list[tuple[str, str]]:
    """Bridges: edges whose removal disconnects (tree edges in outerplanar case)."""
    bridges: list[tuple[str, str]] = []
    for e in g.edges:
        remaining = [x for x in g.edges if x.edge_id != e.edge_id]
        if not _connected(g.vertex_ids, remaining):
            bridges.append((e.u, e.v))
    return bridges


def _connected(vertices: list[str], edges) -> bool:
    if not vertices:
        return True
    adj: dict[str, list[str]] = {v: [] for v in vertices}
    for e in edges:
        adj.setdefault(e.u, []).append(e.v)
        adj.setdefault(e.v, []).append(e.u)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        u = stack.pop()
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(vertices)


def decompose_blocks(g: GateGraph) -> BlockDecomposition:
    """
    Decompose G_C into blocks, cut vertices, bridges, leaf blocks.

    For outerplanar chord graphs, each block is a fan or single edge.
    """
    bridges = _find_bridges(g)
    bridge_set = {tuple(sorted(b)) for b in bridges}
    blocks: list[BiconnectedBlock] = []
    used_edges: set[str] = set()
    bid = 0
    for e in g.edges:
        if e.edge_id in used_edges:
            continue
        if tuple(sorted((e.u, e.v))) in bridge_set:
            blocks.append(
                BiconnectedBlock(
                    block_id=f"B{bid}",
                    vertices=[e.u, e.v],
                    edges=[e.edge_id],
                    is_leaf=True,
                    is_bridge=True,
                )
            )
            used_edges.add(e.edge_id)
            bid += 1
            continue
        verts = {e.u, e.v}
        edge_ids = [e.edge_id]
        used_edges.add(e.edge_id)
        changed = True
        while changed:
            changed = False
            for e2 in g.edges:
                if e2.edge_id in used_edges:
                    continue
                if e2.u in verts or e2.v in verts:
                    verts.add(e2.u)
                    verts.add(e2.v)
                    edge_ids.append(e2.edge_id)
                    used_edges.add(e2.edge_id)
                    changed = True
        degree: dict[str, int] = {v: 0 for v in verts}
        for eid in edge_ids:
            ee = next(x for x in g.edges if x.edge_id == eid)
            degree[ee.u] = degree.get(ee.u, 0) + 1
            degree[ee.v] = degree.get(ee.v, 0) + 1
        cut_verts = [v for v, d in degree.items() if d >= 3]
        is_leaf = len(edge_ids) == 1 and len(cut_verts) == 0
        blocks.append(
            BiconnectedBlock(
                block_id=f"B{bid}",
                vertices=sorted(verts),
                edges=edge_ids,
                is_leaf=is_leaf,
                is_bridge=False,
            )
        )
        bid += 1
    cut_vertices: list[str] = []
    for v in g.vertex_ids:
        block_count = sum(1 for b in blocks if v in b.vertices)
        if block_count >= 2:
            cut_vertices.append(v)
    leaf_blocks = [b for b in blocks if b.is_leaf]
    return BlockDecomposition(
        blocks=blocks,
        cut_vertices=cut_vertices,
        bridges=bridges,
        leaf_blocks=leaf_blocks,
    )
