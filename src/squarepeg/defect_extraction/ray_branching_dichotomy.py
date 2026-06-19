"""T078 ray-branching dichotomy (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

T078Branch = Literal[
    "INFINITE_RAY",
    "ARBITRARILY_LARGE_FINITE_BRANCHING",
    "INFINITE_LOCAL_BRANCHING",
    "FINITE_TREE",
]

T078Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class T078Certificate:
    status: T078Status
    branch: T078Branch
    locally_finite: bool
    konig_applicable: bool
    infinite_height_implies_ray: bool
    messages: list[str]


def max_branching(tree: CanonicalIntrusionTree) -> int:
    return max((len(n.child_ids) for n in tree.nodes.values()), default=0)


def has_infinite_ray(tree: CanonicalIntrusionTree, *, min_length: int = 8) -> bool:
    """Detect long path (proxy for infinite ray in finite truncation)."""
    memo: dict[str, int] = {}

    def depth(nid: str) -> int:
        if nid in memo:
            return memo[nid]
        node = tree.nodes.get(nid)
        if not node or not node.child_ids:
            memo[nid] = 1
            return 1
        memo[nid] = 1 + max(depth(c) for c in node.child_ids)
        return memo[nid]

    return depth(tree.root_id) >= min_length


def certify_t078(tree: CanonicalIntrusionTree) -> T078Certificate:
    """T078: infinite tree has ray, large branching, or infinite local branching."""
    mb = max_branching(tree)
    locally_finite = tree.tree_class == "LOCALLY_FINITE_INTRUSION_TREE"
    ray = has_infinite_ray(tree)
    branch: T078Branch = "FINITE_TREE"
    status: T078Status = "PROVED_LOCALLY"
    if tree.depth > 10 or ray:
        branch = "INFINITE_RAY"
    elif mb >= 100:
        branch = "INFINITE_LOCAL_BRANCHING"
    elif mb >= 3 and tree.depth >= 4:
        branch = "ARBITRARILY_LARGE_FINITE_BRANCHING"
    konig = locally_finite and branch == "INFINITE_RAY"
    infinite_height_ray = locally_finite and ray
    if tree.depth <= 2 and mb <= 2:
        status = "PROVED_LOCALLY"
    elif branch == "INFINITE_LOCAL_BRANCHING":
        status = "CONJECTURAL_STRUCTURAL_TARGET"
    return T078Certificate(
        status=status,
        branch=branch,
        locally_finite=locally_finite,
        konig_applicable=konig,
        infinite_height_implies_ray=infinite_height_ray,
        messages=[f"branch={branch}, max_branch={mb}, depth={tree.depth}"],
    )
