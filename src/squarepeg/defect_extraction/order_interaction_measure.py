"""Order interaction measures Xi_n and Sigma (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.countable_block_increments import block_variation, cross_block_area
from squarepeg.defect_extraction.measurable_order_blocks import MonotoneBlock

FailureClass = Literal[
    "LINEAR_MASS_NONSUMMABLE",
    "CROSS_SIGNATURE_NONSUMMABLE",
    "INTERNAL_BLOCK_NONSUMMABLE",
    "MULTIPLE_FAILURES",
    "NONE",
]


@dataclass
class InteractionAtom:
    block_i: str
    block_j: str
    area: float
    center: tuple[float, float]
    weight: float


@dataclass
class OrderInteractionMeasure:
    xi_total: float
    sigma_tail: float
    atoms: list[InteractionAtom]
    failure_class: FailureClass


def sigma_tail_signature(blocks: list[MonotoneBlock], N: int, *, delta: float = 0.1) -> float:
    """Sigma_n(J;N) = sum_{max(i,j)>N} |A_ij(J)|."""
    incs = [block_variation(b, scale=delta) for b in blocks]
    total = 0.0
    for i in range(N, len(incs)):
        for j in range(i + 1, len(incs)):
            total += cross_block_area(incs[i], incs[j]).A_ij
    return total


def build_interaction_measure(
    blocks: list[MonotoneBlock],
    N: int,
    *,
    delta: float = 0.1,
) -> OrderInteractionMeasure:
    incs = [block_variation(b, scale=delta) for b in blocks]
    atoms: list[InteractionAtom] = []
    xi = 0.0
    for i in range(len(incs)):
        for j in range(i + 1, len(incs)):
            pair = cross_block_area(incs[i], incs[j])
            xi += pair.A_ij
            cx = (i + j) / max(len(incs), 1) * 0.1
            atoms.append(
                InteractionAtom(
                    block_i=incs[i].block_id,
                    block_j=incs[j].block_id,
                    area=pair.A_ij,
                    center=(cx, 0.0),
                    weight=blocks[i].gate_mass * blocks[j].gate_mass,
                )
            )
    sigma = sigma_tail_signature(blocks, N, delta=delta)
    linear_tail = sum(incs[k].V_j for k in range(N, len(incs)))
    failure: FailureClass = "NONE"
    if sigma > 0.1 and linear_tail > 0.1:
        failure = "MULTIPLE_FAILURES"
    elif sigma > 0.08:
        failure = "CROSS_SIGNATURE_NONSUMMABLE"
    elif linear_tail > 0.15:
        failure = "LINEAR_MASS_NONSUMMABLE"
    elif any(incs[k].A_j > 0.2 for k in range(N, len(incs))):
        failure = "INTERNAL_BLOCK_NONSUMMABLE"
    return OrderInteractionMeasure(xi, sigma, atoms, failure)
