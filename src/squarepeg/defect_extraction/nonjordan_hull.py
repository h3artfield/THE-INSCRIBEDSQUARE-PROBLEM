"""Non-Jordan saturation hull classification (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

HullObstruction = Literal[
    "PINCHED_BOUNDARY",
    "MULTIPLE_BOUNDARY_COMPONENTS",
    "TOUCHING_COMPLEMENTARY",
    "DENSE_BOUNDARY_CONTACTS",
    "DISCONNECTED_INTERIOR",
    "SEAM_ARTIFACT",
    "NONE",
]

RepairStatus = Literal["REPAIRABLE_BY_FILLING", "GENUINE_OBSTRUCTION"]


@dataclass
class HullAudit:
    is_jordan_disk: bool
    simply_connected: bool
    obstructions: list[HullObstruction]
    repair: RepairStatus
    messages: list[str]


def classify_hull(
    *,
    is_jordan_disk: bool,
    simply_connected: bool,
    boundary_components: int = 1,
    pinch_points: int = 0,
    seam_artifact: bool = False,
) -> HullAudit:
    """Classify non-Jordan saturation hull failures from Directive 028."""
    obstructions: list[HullObstruction] = []
    if not is_jordan_disk:
        if pinch_points > 0:
            obstructions.append("PINCHED_BOUNDARY")
        if boundary_components > 1:
            obstructions.append("MULTIPLE_BOUNDARY_COMPONENTS")
        if not obstructions:
            obstructions.append("DENSE_BOUNDARY_CONTACTS")
    if seam_artifact:
        obstructions.append("SEAM_ARTIFACT")
    if not simply_connected:
        obstructions.append("DISCONNECTED_INTERIOR")
    repair: RepairStatus = "GENUINE_OBSTRUCTION"
    if obstructions == ["TOUCHING_COMPLEMENTARY"] or (
        simply_connected and boundary_components > 1 and pinch_points == 0
    ):
        repair = "REPAIRABLE_BY_FILLING"
    elif obstructions == ["SEAM_ARTIFACT"]:
        repair = "REPAIRABLE_BY_FILLING"
    return HullAudit(
        is_jordan_disk=is_jordan_disk,
        simply_connected=simply_connected,
        obstructions=obstructions or ["NONE"],
        repair=repair,
        messages=[f"Obstructions: {obstructions}"] if obstructions else ["Jordan disk"],
    )
