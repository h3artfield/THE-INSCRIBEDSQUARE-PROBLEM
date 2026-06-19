"""Diffuse nested winding layers (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.winding_layer_tree import WindingLayerTree, build_layer_tree
from squarepeg.defect_extraction.winding_layers import build_winding_layers

ScaleBranch = Literal[
    "UNIFORM_CONTRACTION",
    "SLOW_CONTRACTION",
    "SCALE_JUMP",
    "MULTICENTER_DRIFT",
]


@dataclass
class NestedChain:
    diameters: list[float]
    lambda_ratios: list[float]
    depth: int
    branch: ScaleBranch


@dataclass
class DiffuseLayerAudit:
    unbounded_depth: bool
    chain: NestedChain | None
    returns_to_t064: bool
    annular_candidate: bool
    messages: list[str]


def build_nested_chain(layers) -> NestedChain:
    diameters = [layer.components[0].diameter if layer.components else 0.1 for layer in layers]
    ratios: list[float] = []
    for i in range(len(diameters) - 1):
        if diameters[i] > 0:
            ratios.append(diameters[i + 1] / diameters[i])
    branch: ScaleBranch = "UNIFORM_CONTRACTION"
    if ratios:
        avg = sum(ratios) / len(ratios)
        if avg < 0.5:
            branch = "SCALE_JUMP"
        elif avg > 0.95:
            branch = "SLOW_CONTRACTION"
        elif len(set(round(r, 1) for r in ratios)) > 2:
            branch = "MULTICENTER_DRIFT"
    return NestedChain(diameters=diameters, lambda_ratios=ratios, depth=len(layers), branch=branch)


def audit_diffuse_layers(layers, *, min_depth: int = 3) -> DiffuseLayerAudit:
    """Diffuse regime: winding depth d_n -> infty or bounded W^+."""
    tree = build_layer_tree(layers)
    chain = build_nested_chain(layers) if layers else None
    unbounded = tree.depth >= min_depth
    returns_t064 = chain.branch == "SCALE_JUMP" if chain else False
    annular = chain.branch in ("UNIFORM_CONTRACTION", "SLOW_CONTRACTION") if chain else False
    msgs = [f"Depth={tree.depth}, branch={chain.branch if chain else 'none'}"]
    return DiffuseLayerAudit(
        unbounded_depth=unbounded,
        chain=chain,
        returns_to_t064=returns_t064,
        annular_candidate=annular,
        messages=msgs,
    )
