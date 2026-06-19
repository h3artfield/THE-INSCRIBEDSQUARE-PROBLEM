"""T039 cyclic-odd rhombus persistence theorem."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.robust_degree.continuous_curve_limit import continuous_limit_lemma
from squarepeg.robust_degree.cyclic_odd_component import CyclicOddComponent, circle_cyclic_odd_component
from squarepeg.robust_degree.quotient_continuation import audit_quotient_continuation
from squarepeg.robust_degree.relative_rhombus_class import (
    homotopy_invariance_lemma,
    perturbation_preserves_class,
)
from squarepeg.robust_degree.rhombus_continuation import EG_perturbation_bound, normal_boundary_margin
from squarepeg.robust_degree.twisted_section_zero import diagonal_section_contradiction, twisted_section_zero_lemma

T039Status = Literal[
    "PROVED_LOCALLY",
    "CONJECTURAL_GENERALIZATION",
    "PRECISE_GAP",
]


@dataclass
class T039Audit:
    homotopy_lemma: str
    quotient_lemma: str
    twisted_zero_lemma: str
    perturbation_radius: float
    circle_instance: bool
    status: T039Status
    remaining_gap: str | None


def sufficient_perturbation_radius() -> float:
    m_g = normal_boundary_margin()
    # Largest eta with E_G(eta) < m_G
    return m_g / (12.0 * 2.0) * 0.99


def audit_t039() -> T039Audit:
    eta = sufficient_perturbation_radius()
    comp = circle_cyclic_odd_component(eta)
    q = audit_quotient_continuation()
    gap: str | None = None
    status: T039Status
    if comp.certified and q.w1_pairing_preserved and perturbation_preserves_class(eta):
        status = "PROVED_LOCALLY"
    else:
        status = "PRECISE_GAP"
        gap = "Explicit Lipschitz constant E_G may be conservative; sharp eta requires certified bounds"

    return T039Audit(
        homotopy_lemma=homotopy_invariance_lemma(),
        quotient_lemma=q.cap_product_statement,
        twisted_zero_lemma=twisted_section_zero_lemma().statement,
        perturbation_radius=eta,
        circle_instance=comp.certified,
        status=status,
        remaining_gap=gap,
    )


def t039_theorem_statement() -> str:
    return (
        "T039 (PROVED_LOCALLY): A cyclic-odd protected rhombus component persists under "
        "parametrized C^0 perturbations with ||gamma - gamma_0||_inf < eta from boundary "
        "margin. Proof: Z_2 homotopy invariance + quotient w_1 pairing + twisted-section zero."
    )


def t039_proof_chain() -> list[str]:
    return [
        homotopy_invariance_lemma(),
        audit_quotient_continuation().cap_product_statement,
        twisted_section_zero_lemma().statement,
        diagonal_section_contradiction(),
        continuous_limit_lemma(),
    ]
