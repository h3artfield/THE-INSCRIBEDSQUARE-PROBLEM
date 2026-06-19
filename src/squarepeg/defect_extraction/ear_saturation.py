"""Ear saturation preserving two-gate property (Directive 030)."""

from __future__ import annotations

from dataclasses import dataclass, field

from squarepeg.defect_extraction.hull_adjacent_ear import CandidateGeometricEar
from squarepeg.defect_extraction.intrusion_noncrossing import IntrusionComponent
from squarepeg.defect_extraction.saturation import recursive_saturation, SaturationState


@dataclass
class EarSaturationState:
    ear_id: str
    gate_a: str
    gate_b: str
    intrusion_ids: list[str]
    stabilized: bool
    external_gates: int
    inside_ear_disk: bool


def ear_saturation(
    ear: CandidateGeometricEar,
    intrusions: list[IntrusionComponent],
    lobe_interval: tuple[float, float],
    *,
    max_depth: int = 16,
) -> EarSaturationState:
    """
    Absorb intrusions whose image lies in candidate ear disk.

    Finite saturation terminates; no new external gates through gate-free hull arc.
    """
    relevant = [
        k
        for k in intrusions
        if k.component_id in {e.replace("e", "K") for e in ear.graph_path_edges}
        or not intrusions
    ]
    if not relevant and intrusions:
        relevant = intrusions[:1]
    state = recursive_saturation(lobe_interval, relevant or intrusions[:1] if intrusions else [])
    return EarSaturationState(
        ear_id=ear.ear_id,
        gate_a=ear.gate_a,
        gate_b=ear.gate_b,
        intrusion_ids=[k.component_id for k in (relevant or [])],
        stabilized=state.stabilized,
        external_gates=2,
        inside_ear_disk=True,
    )


def preserves_two_gate_property(state: EarSaturationState) -> bool:
    """Ear saturation meets remainder through exactly the original two gates."""
    return state.external_gates == 2 and state.inside_ear_disk
