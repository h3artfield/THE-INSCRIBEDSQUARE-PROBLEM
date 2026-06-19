"""T076 nonsummable order-tail trichotomy (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.intrinsic_order_tail import audit_intrinsic_nonsummability
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable
from squarepeg.defect_extraction.order_interaction_measure import build_interaction_measure

T076Branch = Literal[
    "CONCENTRATED_ORDER_INTERACTION",
    "FINITE_CENTER_ORDER_INTERACTION",
    "DIFFUSE_ORDER_INTERACTION",
    "INFINITE_INTRUSION_OR_NONJORDAN",
]

T076Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]


@dataclass
class ConcentrationProfile:
    rho: float
    center: tuple[float, float]
    mass_fraction: float


@dataclass
class T076Certificate:
    status: T076Status
    branch: T076Branch
    intrinsic_nonsummable: bool
    concentration: ConcentrationProfile | None
    center_count: int
    messages: list[str]


def cross_signature_concentration(
    measure,
    *,
    rho: float = 0.2,
) -> ConcentrationProfile | None:
    if not measure.atoms:
        return None
    best = (0.0, (0.0, 0.0))
    total = sum(a.area for a in measure.atoms) or 1.0
    for atom in measure.atoms:
        local = sum(
            a.area
            for a in measure.atoms
            if ((a.center[0] - atom.center[0]) ** 2 + (a.center[1] - atom.center[1]) ** 2) ** 0.5 <= rho
        )
        if local > best[0]:
            best = (local, atom.center)
    frac = best[0] / total
    if frac >= 0.25:
        return ConcentrationProfile(rho=rho, center=best[1], mass_fraction=frac)
    return None


def count_interaction_centers(measure, *, threshold: float = 0.3) -> int:
    if not measure.atoms:
        return 0
    centers = sorted(set((round(a.center[0], 1), round(a.center[1], 1)) for a in measure.atoms))
    clusters = 1
    for i in range(1, len(centers)):
        if abs(centers[i][0] - centers[i - 1][0]) > threshold:
            clusters += 1
    return clusters


def certify_t076(
    gate_set: InfiniteGateSet,
    *,
    K: int = 4,
    eta_0: float = 0.05,
) -> T076Certificate:
    """T076: nonsummable order-tail trichotomy."""
    intrinsic = audit_intrinsic_nonsummability(gate_set, eta_0=eta_0)
    decomp = extend_decomposition_to_countable(gate_set, target_blocks=16)
    measure = build_interaction_measure(decomp.blocks, N=4)
    conc = cross_signature_concentration(measure)
    centers = count_interaction_centers(measure)
    branch: T076Branch = "DIFFUSE_ORDER_INTERACTION"
    status: T076Status = "CONJECTURAL_STRUCTURAL_TARGET"
    if not intrinsic.nonsummable:
        branch = "FINITE_CENTER_ORDER_INTERACTION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif conc and conc.mass_fraction >= 0.3:
        branch = "CONCENTRATED_ORDER_INTERACTION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers <= K:
        branch = "FINITE_CENTER_ORDER_INTERACTION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif measure.sigma_tail > 0.5:
        branch = "INFINITE_INTRUSION_OR_NONJORDAN"
    return T076Certificate(
        status=status,
        branch=branch,
        intrinsic_nonsummable=intrinsic.nonsummable,
        concentration=conc,
        center_count=centers,
        messages=[f"branch={branch}, centers={centers}"],
    )
