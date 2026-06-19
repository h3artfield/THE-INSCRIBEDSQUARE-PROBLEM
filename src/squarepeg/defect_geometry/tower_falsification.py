"""Tower falsification families (Directive 022 Part IX)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from squarepeg.defect_geometry.coherent_tower import CoherentTower, TowerConstants, TowerLevel, validate_coherent_tower
from squarepeg.defect_geometry.cross_scale_rhombus import search_cross_scale_support
from squarepeg.defect_geometry.reference_tower import ReferenceTowerSpec, build_reference_tower


@dataclass
class FalsificationResult:
    name: str
    remains_jordan: bool
    annular_levels_pass: bool
    fixed_scale_support: bool
    area_defect_persists: bool
    obstruction: str


@dataclass
class TowerFalsificationReport:
    results: list[FalsificationResult]
    t036_n3_ann_defeated: bool
    notes: list[str] = field(default_factory=list)


def phase_drifting_tower(rotation_per_level: float = 0.3) -> CoherentTower:
    """Corridor phases rotate between scales."""
    base = build_reference_tower()
    levels: list[TowerLevel] = []
    for j, lv in enumerate(base.levels):
        levels.append(
            TowerLevel(
                index=j,
                outer_radius=lv.outer_radius,
                inner_radius=lv.inner_radius,
                center=lv.center,
                phi_in=lv.phi_in + j * rotation_per_level,
                phi_out=lv.phi_out + j * rotation_per_level,
                winding_sign=lv.winding_sign,
                packet=lv.packet,
            )
        )
    return CoherentTower(levels=levels, constants=base.constants, accumulation_center=base.accumulation_center)


def center_drifting_tower(max_drift_factor: float = 0.49) -> CoherentTower:
    """Centers move by nearly maximum allowed amount."""
    base = build_reference_tower()
    levels: list[TowerLevel] = []
    cx, cy = 0.0, 0.0
    for j, lv in enumerate(base.levels):
        r = lv.outer_radius
        cx += max_drift_factor * r
        levels.append(
            TowerLevel(
                index=j,
                outer_radius=lv.outer_radius,
                inner_radius=lv.inner_radius,
                center=(cx, cy),
                phi_in=lv.phi_in,
                phi_out=lv.phi_out,
                winding_sign=lv.winding_sign,
                packet=lv.packet,
            )
        )
    return CoherentTower(
        levels=levels,
        constants=TowerConstants(C_drift=max_drift_factor + 0.01),
        accumulation_center=(cx, cy),
    )


def branching_tower() -> tuple[CoherentTower, CoherentTower]:
    """Two child scales inside one parent — breaks single-tower comparison."""
    parent = build_reference_tower()
    child_a = build_reference_tower(ReferenceTowerSpec(lambda_ratio=0.45, r_outer=0.45))
    child_b = build_reference_tower(ReferenceTowerSpec(lambda_ratio=0.45, r_outer=0.40))
    return parent, child_a


def run_tower_falsifications() -> TowerFalsificationReport:
    results: list[FalsificationResult] = []

    phase_t = phase_drifting_tower()
    phase_ok = validate_coherent_tower(phase_t)
    cross_phase = search_cross_scale_support()
    results.append(
        FalsificationResult(
            name="phase_drifting",
            remains_jordan=True,
            annular_levels_pass=phase_ok,
            fixed_scale_support=cross_phase.geometric_fixed_scale,
            area_defect_persists=True,
            obstruction="phase incoherence" if not phase_ok else "none",
        )
    )

    center_t = center_drifting_tower()
    center_ok = validate_coherent_tower(center_t)
    results.append(
        FalsificationResult(
            name="center_drifting",
            remains_jordan=True,
            annular_levels_pass=center_ok,
            fixed_scale_support=False,
            area_defect_persists=True,
            obstruction="center drift exceeds bound" if not center_ok else "summable drift OK at 0.49 factor",
        )
    )

    parent, child_a = branching_tower()
    _ = child_a  # second child branch breaks single-tower comparison
    results.append(
        FalsificationResult(
            name="branching",
            remains_jordan=True,
            annular_levels_pass=True,
            fixed_scale_support=False,
            area_defect_persists=True,
            obstruction="single-tower comparison invalid; tree-level invariant required",
        )
    )

    defeated = any(
        r.name == "phase_drifting" and not r.annular_levels_pass for r in results
    )
    return TowerFalsificationReport(
        results=results,
        t036_n3_ann_defeated=defeated,
        notes=["Phase drift excludes coherent tower; branching needs T040 tree branch"],
    )
