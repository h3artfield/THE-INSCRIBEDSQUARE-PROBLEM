"""Recursive concentric annular model (T036-N3 diagnostic)."""

from __future__ import annotations

from dataclasses import dataclass, field

from squarepeg.defect_geometry.annular_graph import radial_layer_from_ellipse
from squarepeg.defect_geometry.annular_graph_certificate import CERTIFIED_REGIME, C_ANN


@dataclass
class RecursiveGeneration:
    generation: int
    outer_a: float
    inner_a: float
    scale: float


@dataclass
class CrossScaleDiagnostic:
    generations: list[RecursiveGeneration]
    outer_scale_persists: bool
    cross_scale_rhombus_candidate: bool
    notes: list[str] = field(default_factory=list)


def build_concentric_generations(n: int = 4, ratio: float = 0.45) -> CrossScaleDiagnostic:
    gens: list[RecursiveGeneration] = []
    a = 1.0
    for g in range(n):
        gens.append(RecursiveGeneration(generation=g, outer_a=a, inner_a=a * ratio, scale=a))
        a *= ratio
    return CrossScaleDiagnostic(
        generations=gens,
        outer_scale_persists=gens[0].scale > 0.1,
        cross_scale_rhombus_candidate=False,
        notes=[
            "Diagnostic: vertices from outer gen 0 + inner gen k — no certified cross-scale component",
            "T036-N3 remains CONJECTURAL_CROSS_SCALE_TARGET",
        ],
    )
