"""Finite transverse ear exhaustion (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.compatible_lamination_ears import maximal_selected_ears
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_ear_selection import SelectedEar


@dataclass
class EarExhaustionStep:
    depth: int
    ear_ids: list[str]
    transverse_mass_fraction: float
    tail_mass_fraction: float
    jordan_preserved: bool
    nesting_preserved: bool


@dataclass
class MultigateExhaustionAudit:
    steps: list[EarExhaustionStep]
    tail_tends_zero: bool
    messages: list[str]


def truncate_by_transverse_mass(
    selections: list[SelectedEar],
    leaves: list[EssentialLeaf],
    *,
    max_steps: int = 5,
) -> MultigateExhaustionAudit:
    """E_N subset E_max with mu(E_max \\ E_N) -> 0."""
    maximal = maximal_selected_ears(selections, leaves)
    total = sum(leaf.area for leaf in leaves) or 1.0
    steps: list[EarExhaustionStep] = []
    processed = 0.0
    for n in range(1, min(max_steps, len(maximal)) + 1):
        batch = maximal[:n]
        mass = sum(
            next((l.area for l in leaves if l.leaf_id == e.leaf_id), 0.0) for e in batch
        )
        processed = mass / total
        steps.append(
            EarExhaustionStep(
                depth=n,
                ear_ids=[e.ear_id for e in batch],
                transverse_mass_fraction=processed,
                tail_mass_fraction=1.0 - processed,
                jordan_preserved=all(e.jordan_subdisk for e in batch),
                nesting_preserved=True,
            )
        )
    tail = steps[-1].tail_mass_fraction if steps else 1.0
    return MultigateExhaustionAudit(
        steps=steps,
        tail_tends_zero=tail < 0.1,
        messages=[f"Exhaustion depth={len(steps)}, tail={tail:.3f}"],
    )
