"""Defect forest extraction (T040/T045) (Directive 023)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.nested_forest import PacketForest, forest_is_admissible
from squarepeg.defect_surgery.packet_disk import PacketDisk

ExtractionResult = Literal[
    "ISOLATED_CARLESON_FOREST",
    "NONISOLATED_PACKET",
    "UNBOUNDED_OVERLAP",
    "BRANCHING_WITHOUT_CARLESON_CONTROL",
    "NO_JORDAN_CROSSCUT",
    "UNRESOLVED",
]


@dataclass
class DefectForestExtraction:
    classification: ExtractionResult
    forest: PacketForest | None
    positive_scale: bool
    messages: list[str]


def extract_defect_forest(
    disks: list[PacketDisk],
    *,
    scales: list[float] | None = None,
) -> DefectForestExtraction:
    """T045 reconnaissance: classify persistent defect packet arrangement."""
    if not disks:
        return DefectForestExtraction("UNRESOLVED", None, False, ["No disks"])

    forest = PacketForest(disks=disks)
    scales = scales or [d.diameter for d in disks]
    limsup = max(scales[-5:]) if len(scales) >= 5 else max(scales)
    if limsup > 0.05:
        return DefectForestExtraction(
            "UNRESOLVED",
            forest,
            True,
            ["Positive-scale branch: T036-N1-ANN applies"],
        )

    if not forest_is_admissible(forest):
        return DefectForestExtraction(
            "UNBOUNDED_OVERLAP",
            None,
            False,
            ["Disks neither disjoint nor nested"],
        )

    from squarepeg.defect_surgery.carleson_mass import mu_D_on_interval

    dense = mu_D_on_interval(disks, set(range(20))) > 0.5
    if dense:
        return DefectForestExtraction(
            "BRANCHING_WITHOUT_CARLESON_CONTROL",
            forest,
            False,
            ["Carleson mass fails on small intervals"],
        )

    return DefectForestExtraction(
        "ISOLATED_CARLESON_FOREST",
        forest,
        False,
        ["Candidate surgery-admissible forest (extraction not proved from T037)"],
    )


def t045_statement() -> str:
    return (
        "T045 (CONJECTURAL_FULL_EXTRACTION): Persistent defects => positive-scale component or "
        "surgery-admissible forest."
    )
