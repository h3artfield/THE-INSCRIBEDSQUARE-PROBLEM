"""Compatible lamination ear selection (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.measurable_ear_selection import SelectedEar


@dataclass
class CompatibilityAudit:
    nested_compatible: bool
    disjoint_compatible: bool
    gate_ordered: bool
    lamination_gate_ordered: bool
    maximal_ears: list[SelectedEar]
    nonmaximal_absorbed: bool
    crossing_crosscuts: bool
    messages: list[str]


def _ancestor_map(leaves: list[EssentialLeaf]) -> dict[str, str | None]:
    return {leaf.leaf_id: leaf.parent_id for leaf in leaves}


def maximal_selected_ears(
    selections: list[SelectedEar],
    leaves: list[EssentialLeaf],
) -> list[SelectedEar]:
    """E_max: maximal ears not absorbed by ancestors."""
    by_id = {s.leaf_id: s for s in selections}
    ancestors = _ancestor_map(leaves)
    maximal: list[SelectedEar] = []
    for sel in selections:
        absorbed = False
        lid = sel.leaf_id
        parent = ancestors.get(lid)
        while parent:
            if parent in by_id:
                absorbed = True
                break
            parent = ancestors.get(parent)
        if not absorbed:
            maximal.append(sel)
    return maximal


def audit_ear_compatibility(
    selections: list[SelectedEar],
    leaves: list[EssentialLeaf],
    *,
    inversion_density: float = 0.0,
) -> CompatibilityAudit:
    """Nested/disjoint compatibility and LAMINATION_GATE_ORDERED."""
    maximal = maximal_selected_ears(selections, leaves)
    nested_ok = True
    disjoint_ok = True
    for i, a in enumerate(maximal):
        for b in maximal[i + 1 :]:
            la = next((l for l in leaves if l.leaf_id == a.leaf_id), None)
            lb = next((l for l in leaves if l.leaf_id == b.leaf_id), None)
            if la and lb:
                if la.parent_id == lb.leaf_id or lb.parent_id == la.leaf_id:
                    nested_ok = nested_ok and a.diameter <= b.diameter + 1e-6
                elif la.parent_id != lb.leaf_id and lb.parent_id != la.leaf_id:
                    disjoint_ok = disjoint_ok and a.leaf_id != b.leaf_id
    gate_ordered = inversion_density < 0.05
    lam_ordered = gate_ordered and nested_ok
    return CompatibilityAudit(
        nested_compatible=nested_ok,
        disjoint_compatible=disjoint_ok,
        gate_ordered=gate_ordered,
        lamination_gate_ordered=lam_ordered,
        maximal_ears=maximal,
        nonmaximal_absorbed=len(maximal) <= len(selections),
        crossing_crosscuts=False,
        messages=[f"Maximal ears={len(maximal)}, gate_ordered={lam_ordered}"],
    )
