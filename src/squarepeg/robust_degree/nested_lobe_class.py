"""Nested same-sign lobe class D_nest for T036-N."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from squarepeg.robust_degree.defect_lobe_tree import DefectLobeTree, LobeNode


@dataclass
class NestedLobeClass:
    lambda_minus: float = 0.25
    lambda_plus: float = 0.75
    min_separation: float = 0.01
    min_chain_length: int = 2


def belongs_to_D_nest(tree: DefectLobeTree, cfg: NestedLobeClass | None = None) -> bool:
    """Check nested same-sign lobe chain with diameter ratio bounds."""
    c = cfg or NestedLobeClass()

    def find_chain(node: LobeNode, chain: list[LobeNode]) -> list[LobeNode]:
        best = chain + [node]
        for ch in node.children:
            if ch.winding_sign == node.winding_sign:
                cand = find_chain(ch, best)
                if len(cand) > len(best):
                    best = cand
        return best

    chain = find_chain(tree.root, [])
    if len(chain) < c.min_chain_length:
        return False
    for i in range(len(chain) - 1):
        d0 = chain[i].diameter
        d1 = chain[i + 1].diameter
        if d0 <= 0:
            return False
        ratio = d1 / d0
        if ratio < c.lambda_minus or ratio > c.lambda_plus:
            return False
    return True


def t036_n_statement() -> str:
    return (
        "T036-N (CONTROLLED_CLASS_TARGET): For defect packets in D_nest, "
        "either fixed-scale protected square/family OR area-tight subsequence."
    )
