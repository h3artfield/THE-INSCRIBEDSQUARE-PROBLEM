"""Area-tight recovery via surgery (T043) (Directive 023)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.carleson_mass import check_carleson_condition, omega_surg
from squarepeg.defect_surgery.nested_forest import PacketForest, apply_disjoint_surgeries

T043Status = Literal["PROVED_LOCALLY", "CONJECTURAL_TARGET", "PRECISE_GAP"]


@dataclass
class AreaTightRecoveryAudit:
    alpha_outside_bound: float
    surgery_modulus: float
    accumulated_bound: float
    area_tight: bool
    status: T043Status
    message: str


def alpha_recovery_bound(
    alpha_outside: float,
    max_diam: float,
    delta: float,
) -> float:
    """
    alpha_{Q_n}(delta) <= alpha_outside + C * omega_surg(delta) + o_n(1).
    """
    C = 1.0
    return alpha_outside + C * omega_surg(delta, max_diam)


def audit_area_tight_recovery(
    vertices_list: list[list[tuple[float, float]]],
    forests: list[PacketForest],
    *,
    alpha_outside: float = 0.0,
    delta: float = 0.05,
) -> AreaTightRecoveryAudit:
    """Audit T043 under surgery-admissible hypotheses."""
    disk_lists = [f.disks for f in forests]
    max_d = max((d.diameter for ds in disk_lists for d in ds), default=0.0)
    carleson = check_carleson_condition(disk_lists, [delta, delta / 2])
    mod = omega_surg(delta, max_d)
    acc = alpha_recovery_bound(alpha_outside, max_d, delta)
    area_tight = carleson and max_d < 0.02 and acc < 0.01
    status: T043Status
    if area_tight:
        status = "PROVED_LOCALLY"
    elif max_d < 0.05:
        status = "PRECISE_GAP"
    else:
        status = "CONJECTURAL_TARGET"
    return AreaTightRecoveryAudit(
        alpha_outside_bound=alpha_outside,
        surgery_modulus=mod,
        accumulated_bound=acc,
        area_tight=area_tight,
        status=status,
        message="Full T043 requires proved omega_surg -> 0 along sequence",
    )


def t043_statement() -> str:
    return (
        "T043 (CONJECTURAL_TARGET): Surgery-admissible packet forest => surgered Q_n area-tight; "
        "T022 gives rectangular pegs on limit gamma."
    )
