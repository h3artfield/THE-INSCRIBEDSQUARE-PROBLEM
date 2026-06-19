"""Nested same-sign chain in D_nest."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_geometry.lobe import LobeRecord, area_fullness, scale_ratio
from squarepeg.defect_geometry.lobe_tree import LobeTree


@dataclass(frozen=True)
class NestedClassParams:
    """Quantitative constants for D_nest(m, lambda-, lambda+, delta_sep, beta)."""

    lambda_minus: float = 0.25
    lambda_plus: float = 0.75
    delta_sep: float = 0.05
    beta: float = 0.01
    min_depth: int = 2
    area_threshold: float = 0.0


@dataclass
class NestedChain:
    lobes: list[LobeRecord]
    same_orientation: bool
    scale_controlled: bool
    area_full: bool
    depth: int


def find_same_sign_chain(tree: LobeTree) -> NestedChain:
    """Longest same-sign chain L_1 supset ... supset L_m in tree."""

    def walk(node_id: str, chain: list[LobeRecord]) -> list[LobeRecord]:
        node = tree.nodes[node_id]
        best = chain + [node]
        for cid in node.children:
            child = tree.nodes[cid]
            if child.orientation_sign == node.orientation_sign:
                cand = walk(cid, best)
                if len(cand) > len(best):
                    best = cand
        return best

    chain = walk(tree.root.lobe_id, [])
    same = len(set(l.orientation_sign for l in chain)) <= 1 if chain else False
    return NestedChain(
        lobes=chain,
        same_orientation=same,
        scale_controlled=False,
        area_full=False,
        depth=len(chain),
    )


def verify_nested_chain(chain: NestedChain, params: NestedClassParams) -> bool:
    if chain.depth < params.min_depth or not chain.same_orientation:
        return False
    for i in range(len(chain.lobes) - 1):
        r = scale_ratio(chain.lobes[i], chain.lobes[i + 1])
        if r < params.lambda_minus or r > params.lambda_plus:
            return False
        if not area_fullness(chain.lobes[i], params.beta):
            return False
        # Separation: proxy via diameter gap (attachment corridors excluded qualitatively)
        sep = chain.lobes[i].diameter - chain.lobes[i + 1].diameter
        if sep < params.delta_sep * chain.lobes[i].diameter:
            return False
    chain.scale_controlled = True
    chain.area_full = True
    return True


def in_D_nest(tree: LobeTree, params: NestedClassParams | None = None) -> bool:
    p = params or NestedClassParams()
    chain = find_same_sign_chain(tree)
    if abs(tree.root.enclosed_area) < p.area_threshold and p.area_threshold > 0:
        return False
    return verify_nested_chain(chain, p)
