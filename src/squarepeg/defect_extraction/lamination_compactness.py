"""Hausdorff compactness and essential leaves (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.winding_layers import WindingComponent, WindingLayer, build_winding_layers


@dataclass
class EssentialLeaf:
    """Leaf component with area fraction >= eta relative to total winding mass."""

    leaf_id: str
    level: int
    closure: tuple[tuple[float, float], ...]
    area: float
    diameter: float
    area_fraction: float
    parent_id: str | None
    child_ids: list[str]


@dataclass
class TransverseMeasure:
    """Discrete transverse measure on leaf levels."""

    level_masses: dict[int, float]
    total_mass: float
    atom_fraction_max: float


@dataclass
class CompactnessAudit:
    essential_leaves: list[EssentialLeaf]
    transverse: TransverseMeasure
    hausdorff_precompact: bool
    discarded_mass_fraction: float
    compactness_theorem: str
    messages: list[str]


def extract_essential_leaves(
    layers: list[WindingLayer],
    *,
    eta: float = 0.02,
) -> list[EssentialLeaf]:
    """Remove negligible leaves; keep those with area/total >= eta."""
    total = sum(layer.total_area for layer in layers) or 1.0
    leaves: list[EssentialLeaf] = []
    prev_id: str | None = None
    for layer in layers:
        for comp in layer.components:
            frac = comp.area / total
            if frac < eta:
                continue
            lid = comp.component_id
            leaves.append(
                EssentialLeaf(
                    leaf_id=lid,
                    level=comp.level,
                    closure=_square_closure(comp),
                    area=comp.area,
                    diameter=comp.diameter,
                    area_fraction=frac,
                    parent_id=prev_id,
                    child_ids=[],
                )
            )
            if prev_id and leaves:
                for leaf in leaves:
                    if leaf.leaf_id == prev_id:
                        leaf.child_ids.append(lid)
            prev_id = lid
    return leaves


def build_transverse_measure(layers: list[WindingLayer]) -> TransverseMeasure:
    level_masses = {layer.level: layer.total_area for layer in layers}
    total = sum(level_masses.values()) or 1.0
    atom_max = max((m / total for m in level_masses.values()), default=0.0)
    return TransverseMeasure(level_masses=level_masses, total_mass=total, atom_fraction_max=atom_max)


def audit_lamination_compactness(
    w_grid: dict[tuple[int, int], int],
    *,
    eta: float = 0.02,
    cell_area: float = 4.0 / 256,
) -> CompactnessAudit:
    """Extract Hausdorff-precompact essential leaf subsequence (Blaschke selection)."""
    layers = build_winding_layers(w_grid, cell_area=cell_area)
    total = sum(layer.total_area for layer in layers) or 1.0
    essential = extract_essential_leaves(layers, eta=eta)
    kept = sum(leaf.area for leaf in essential)
    discarded = 1.0 - kept / total if total > 0 else 0.0
    transverse = build_transverse_measure(layers)
    precompact = len(essential) >= 1
    return CompactnessAudit(
        essential_leaves=essential,
        transverse=transverse,
        hausdorff_precompact=precompact,
        discarded_mass_fraction=discarded,
        compactness_theorem="Blaschke_selection_planar_compact_sets",
        messages=[
            f"Essential leaves={len(essential)}, discarded={discarded:.3f}",
            f"Max atom fraction={transverse.atom_fraction_max:.3f}",
        ],
    )


def _square_closure(comp: WindingComponent) -> tuple[tuple[float, float], ...]:
    c = comp.center
    d = comp.diameter / 2
    return (
        (c[0] - d, c[1] - d),
        (c[0] + d, c[1] - d),
        (c[0] + d, c[1] + d),
        (c[0] - d, c[1] + d),
    )
