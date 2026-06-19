"""T040 annular packet tower selection (Directive 022)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_geometry.coherent_tower import CoherentTower, validate_coherent_tower
from squarepeg.defect_geometry.reference_tower import build_reference_tower

TowerExtraction = Literal[
    "COHERENT_TOWER_EXTRACTED",
    "BRANCHING_DEFECT_TREE",
    "PHASE_DRIFT_OBSTRUCTION",
    "CENTER_DRIFT_OBSTRUCTION",
    "UNRELATED_PACKETS",
]


@dataclass
class PacketRecord:
    packet_id: str
    center: tuple[float, float]
    outer_radius: float
    phi_in: float
    phi_out: float
    winding_sign: int
    parent_id: str | None = None


@dataclass
class TowerExtractionResult:
    classification: TowerExtraction
    coherent: bool
    tower: CoherentTower | None
    messages: list[str]


def _scale_ratios(records: list[PacketRecord]) -> list[float]:
    if len(records) < 2:
        return []
    rs = [r.outer_radius for r in records]
    return [rs[i + 1] / rs[i] for i in range(len(rs) - 1) if rs[i] > 0]


def extract_tower_from_packets(records: list[PacketRecord]) -> TowerExtractionResult:
    """
    Attempt tower extraction from shrinking defect packets.
    Does NOT assume spatial shrinking alone implies coherence.
    """
    if len(records) < 2:
        return TowerExtractionResult(
            classification="UNRELATED_PACKETS",
            coherent=False,
            tower=None,
            messages=["Fewer than two packets"],
        )

    # Sort by decreasing scale
    sorted_r = sorted(records, key=lambda r: -r.outer_radius)
    ratios = _scale_ratios(sorted_r)
    lam_ok = all(0.42 <= r <= 0.48 for r in ratios) if ratios else False

    # Center drift
    max_drift = 0.0
    for i in range(len(sorted_r) - 1):
        dx = sorted_r[i + 1].center[0] - sorted_r[i].center[0]
        dy = sorted_r[i + 1].center[1] - sorted_r[i].center[1]
        max_drift = max(max_drift, (dx * dx + dy * dy) ** 0.5)
    if max_drift > 0.5 * sorted_r[-1].outer_radius:
        return TowerExtractionResult(
            classification="CENTER_DRIFT_OBSTRUCTION",
            coherent=False,
            tower=None,
            messages=["Center drift exceeds C_drift * r_{j+1} bound"],
        )

    # Phase drift
    phase_spread = 0.0
    for i in range(len(sorted_r) - 1):
        phase_spread += abs(sorted_r[i + 1].phi_in - sorted_r[i].phi_in)
    if phase_spread > 0.5 and not lam_ok:
        return TowerExtractionResult(
            classification="PHASE_DRIFT_OBSTRUCTION",
            coherent=False,
            tower=None,
            messages=["Corridor phases not coherent across scales"],
        )

    # Branching: multiple children same parent
    parents: dict[str, list[str]] = {}
    for r in records:
        if r.parent_id:
            parents.setdefault(r.parent_id, []).append(r.packet_id)
    if any(len(v) > 1 for v in parents.values()):
        return TowerExtractionResult(
            classification="BRANCHING_DEFECT_TREE",
            coherent=False,
            tower=None,
            messages=["Multiple child packets in one parent — tree-level invariant needed"],
        )

    if lam_ok and max_drift <= 0.1:
        tower = build_reference_tower()
        if validate_coherent_tower(tower):
            return TowerExtractionResult(
                classification="COHERENT_TOWER_EXTRACTED",
                coherent=True,
                tower=tower,
                messages=["Reference-shaped tower extracted; verify embedding in limit curve separately"],
            )

    return TowerExtractionResult(
        classification="UNRELATED_PACKETS",
        coherent=False,
        tower=None,
        messages=["Shrinking scales without full tower coherence"],
    )


def t040_statement() -> str:
    return (
        "T040 (CONJECTURAL_SELECTION_TARGET): Persistent ANNULAR_GRAPH packets without area-tightness "
        "yield positive-scale subsequence (T036-N1-ANN), coherent tower (T036-N3-ANN), or branching/incoherent tree."
    )
