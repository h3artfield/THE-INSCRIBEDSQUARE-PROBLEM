"""Gate-tail defect mass (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.finite_gate_truncation import GateTruncation
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.saturated_gate_truncation import SaturatedTruncation


@dataclass
class GateTailDefect:
    leaf_id: str
    level: int
    intrinsic_ear_area: float
    join_terms: float
    gate_interaction: float
    retained_skeleton_correction: float
    total_defect: float


def tail_subsystem_mass(gate_set: InfiniteGateSet, trunc: GateTruncation) -> float:
    """Mass of T_N = C_infty \\ G_N in nu_L support."""
    omitted = gate_set.total_mass * (1.0 - trunc.mass_fraction)
    return omitted


def defect_tail_N(sat: SaturatedTruncation, gate_set: InfiniteGateSet) -> GateTailDefect:
    """DefTail_N(L) including intrinsic, join, interaction, retained corrections."""
    trunc = sat.gate_truncation
    omitted_frac = max(1.0 - trunc.mass_fraction, 0.0)
    omitted_mass = gate_set.total_mass * omitted_frac
    intrinsic = omitted_mass * omitted_frac * 0.4
    join = omitted_mass * omitted_mass * 4.5
    interaction = omitted_mass * len(trunc.gates) * 0.001
    retained = omitted_mass * 0.05 * omitted_frac
    total = intrinsic + join + interaction + retained
    return GateTailDefect(
        leaf_id=sat.leaf_id,
        level=sat.level,
        intrinsic_ear_area=intrinsic,
        join_terms=join,
        gate_interaction=interaction,
        retained_skeleton_correction=retained,
        total_defect=total,
    )
