"""Gate word limits and inversion count (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

OrderClass = Literal["ASYMPTOTICALLY_ORDERED", "PERSISTENTLY_SCRAMBLED", "MIXED"]


@dataclass
class GateWordLimit:
    hull_order: list[str]
    parameter_order: list[str]
    inversion_count: int
    normalized_inversion: float
    order_class: OrderClass


def inversion_count(hull_order: list[str], param_order: list[str]) -> int:
    """Count order inversions between hull and parameter cyclic orders."""
    idx = {g: i for i, g in enumerate(hull_order)}
    mapped = [idx[g] for g in param_order if g in idx]
    inv = 0
    for i in range(len(mapped)):
        for j in range(i + 1, len(mapped)):
            if mapped[i] > mapped[j]:
                inv += 1
    return inv


def normalized_inversion(hull_order: list[str], param_order: list[str]) -> float:
    """Inv(W_n) / M_n^2."""
    m = len(hull_order)
    if m < 2:
        return 0.0
    return inversion_count(hull_order, param_order) / (m * m)


def classify_gate_word(hull_order: list[str], param_order: list[str]) -> GateWordLimit:
    inv = inversion_count(hull_order, param_order)
    norm = normalized_inversion(hull_order, param_order)
    if norm < 0.01:
        oc: OrderClass = "ASYMPTOTICALLY_ORDERED"
    elif norm > 0.05:
        oc = "PERSISTENTLY_SCRAMBLED"
    else:
        oc = "MIXED"
    return GateWordLimit(
        hull_order=hull_order,
        parameter_order=param_order,
        inversion_count=inv,
        normalized_inversion=norm,
        order_class=oc,
    )


def asymptotically_ordered(sequence: list[GateWordLimit]) -> bool:
    return all(g.normalized_inversion < 0.02 for g in sequence[-3:]) if len(sequence) >= 1 else False
