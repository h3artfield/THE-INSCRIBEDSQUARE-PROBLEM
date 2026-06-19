"""Machine-readable signature equality ledger (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

LedgerID = Literal[
    "WEDGE_PRODUCT",
    "TRIANGLE_NORM",
    "CAUCHY_SCHWARZ",
    "CHILD_INCREMENT",
    "HULL_DIAMETER",
    "CROSSCUT_AREA",
    "RETAINED_SKELETON",
    "CENTER_PACKING",
    "FINITE_CENTER_GROUP",
    "SIGN_GROUPING",
    "CORONA_TRUNCATION",
    "MULTIGEN_PACKING",
]


@dataclass(frozen=True)
class LedgerEntry:
    id: LedgerID
    expression: str
    bound: str
    constant: float
    hypotheses: str
    equality_condition: str
    stability: str
    dependency: str


LEDGER: tuple[LedgerEntry, ...] = (
    LedgerEntry(
        "WEDGE_PRODUCT",
        "|a∧b|",
        "≤ |a||b|",
        1.0,
        "vectors in R^2",
        "a ⟂ b or a=0 or b=0",
        "deficit ≤ ε ⟹ angle ≥ arccos(1-ε/|a||b|)",
        "signature_budget.wedge_child_child",
    ),
    LedgerEntry(
        "TRIANGLE_NORM",
        "|a+b|",
        "≤ |a|+|b|",
        1.0,
        "vectors in R^2",
        "a parallel to b, same orientation",
        "deficit ≤ ε ⟹ sin(angle) ≤ ε/(|a|+|b|)",
        "signature_budget.wedge_parent_child",
    ),
    LedgerEntry(
        "CAUCHY_SCHWARZ",
        "|⟨a,b⟩|",
        "≤ |a||b|",
        1.0,
        "inner product",
        "a parallel to b",
        "deficit ≤ ε ⟹ collinearity modulus",
        "child_signature_packing",
    ),
    LedgerEntry(
        "CHILD_INCREMENT",
        "Φ(w)",
        "≤ C Φ(v)",
        1.0,
        "nested Jordan hull w ⊂ v",
        "diam(H_w)/diam(H_v) = gate ratio",
        "near equality ⟹ scale ratio extremal",
        "multigeneration_packing",
    ),
    LedgerEntry(
        "HULL_DIAMETER",
        "diam(H)",
        "≤ 2r",
        2.0,
        "Jordan disk radius r",
        "diameter endpoints on boundary",
        "deficit ⟹ endpoints within ω(ε) of antipodal",
        "endpoint_multifunction",
    ),
    LedgerEntry(
        "CROSSCUT_AREA",
        "A_cross",
        "≤ C L(v)^2",
        0.08,
        "Jordan crosscut",
        "crosscut realizes gate chord",
        "area deficit ⟹ chord near diameter",
        "signature_budget.crosscut",
    ),
    LedgerEntry(
        "RETAINED_SKELETON",
        "m_ret",
        "≤ m(v)",
        1.0,
        "mass partition",
        "all mass in children",
        "retained > 0 ⟹ skeleton obstruction",
        "signature_budget.retained",
    ),
    LedgerEntry(
        "CENTER_PACKING",
        "N_c centers",
        "≤ K",
        4.0,
        "finite-center complexity",
        "single coherent center group",
        "excess centers ⟹ drift ω(ε)",
        "finite_center_density_improvement",
    ),
    LedgerEntry(
        "FINITE_CENTER_GROUP",
        "groups",
        "≤ K",
        4.0,
        "child partition",
        "one dominant group",
        "multi-group ⟹ T062 route",
        "cantor_corona",
    ),
    LedgerEntry(
        "SIGN_GROUPING",
        "signed wedge",
        "≤ sum |wedge|",
        1.0,
        "signed defects",
        "uniform sign or zero",
        "mixed sign ⟹ cancellation excess",
        "signature_excess",
    ),
    LedgerEntry(
        "CORONA_TRUNCATION",
        "tail mass",
        "→ 0",
        0.0,
        "T087 tail",
        "vanishing fine tails",
        "nonzero tail ⟹ Carleson failure",
        "end_signature_carleson",
    ),
    LedgerEntry(
        "MULTIGEN_PACKING",
        "P_L(v)",
        "≤ (1-η)Φ(v)",
        0.949,
        "cov_L ≥ 0.25 signature-scale",
        "P_L = Φ_desc slice equality",
        "neutral when equality in all child terms",
        "multigeneration_packing",
    ),
)


def get_ledger() -> list[LedgerEntry]:
    return list(LEDGER)


def get_entry(ledger_id: LedgerID) -> LedgerEntry:
    for e in LEDGER:
        if e.id == ledger_id:
            return e
    raise KeyError(ledger_id)
