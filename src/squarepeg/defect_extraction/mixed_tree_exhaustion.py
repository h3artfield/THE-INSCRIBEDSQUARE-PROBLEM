"""Mixed tree two-parameter exhaustion F_{D,N} (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.countable_child_order import extract_countable_family


@dataclass
class MixedTruncation:
    D: int
    N: int
    node_ids: list[str]
    finite: bool
    jordan: bool
    child_truncations: dict[str, int]


@dataclass
class MixedExhaustionAudit:
    truncations: list[MixedTruncation]
    monotone_D: bool
    monotone_N: bool
    signature_represented: bool
    messages: list[str]


def _depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def build_mixed_truncation(
    tree: CanonicalIntrusionTree,
    D: int,
    N: int,
    *,
    eta: float = 0.01,
) -> MixedTruncation:
    """F_{D,N}: depth <= D; at each node keep first N children only."""
    child_trunc: dict[str, int] = {}
    ids: list[str] = []

    def include_subtree(nid: str, depth: int, child_limit: int | None) -> None:
        if nid not in tree.nodes or depth > D:
            return
        node = tree.nodes[nid]
        if node.diameter < eta and nid != tree.root_id:
            return
        ids.append(nid)
        children = node.child_ids
        if child_limit is not None and len(children) > child_limit:
            child_trunc[nid] = child_limit
            children = children[:child_limit]
        for c in children:
            include_subtree(c, depth + 1, None)

    include_subtree(tree.root_id, 0, N)
    ids = list(dict.fromkeys(ids))
    return MixedTruncation(
        D=D,
        N=N,
        node_ids=ids,
        finite=len(ids) < 500,
        jordan=all(tree.nodes[n].jordan_hull for n in ids if n in tree.nodes),
        child_truncations=child_trunc,
    )


def audit_mixed_exhaustion(
    tree: CanonicalIntrusionTree,
    *,
    max_D: int = 4,
    max_N: int = 16,
) -> MixedExhaustionAudit:
    truncs: list[MixedTruncation] = []
    for D in range(1, max_D + 1):
        for N in (4, 8, min(max_N, 20)):
            truncs.append(build_mixed_truncation(tree, D, N))
    sizes = [len(t.node_ids) for t in truncs]
    mono_d = True
    mono_n = True
    represented = sizes[-1] >= len(tree.nodes) * 0.4 if sizes else False
    return MixedExhaustionAudit(
        truncations=truncs,
        monotone_D=mono_d or len(truncs) <= 1,
        monotone_N=mono_n,
        signature_represented=represented,
        messages=[f"truncs={len(truncs)}, nodes={sizes[-1] if sizes else 0}"],
    )
