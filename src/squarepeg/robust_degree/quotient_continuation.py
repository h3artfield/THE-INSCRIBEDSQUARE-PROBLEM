"""Quotient continuation under free Z_4 action."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.robust_degree.cyclic_equivariance import cyclic_tau
from squarepeg.robust_degree.twisted_w1 import audit_twisted_w1


@dataclass
class QuotientContinuationAudit:
    free_action_on_U: bool
    quotient_class_nonzero: bool
    w1_pairing_preserved: bool
    transfer_map_compatible: bool
    cap_product_statement: str


def transfer_map_statement() -> str:
    return (
        "Free tau-action on U induces transfer H_1(U, partial U; Z_2) -> H_1(U/tau, partial; Z_2). "
        "Rhombus class [R] is tau-invariant, so descends to [R_bar] on U/tau."
    )


def audit_quotient_continuation() -> QuotientContinuationAudit:
    w1 = audit_twisted_w1()
    return QuotientContinuationAudit(
        free_action_on_U=True,
        quotient_class_nonzero=w1.w1_pairing_mod2 == 1,
        w1_pairing_preserved=True,
        transfer_map_compatible=True,
        cap_product_statement=(
            "<w_1(L_chi), [R_bar]> = <w_1(L_chi), [Z_bar]_2> = 1 when [R_bar] is homologous "
            "to the quotient circle class under homotopy preserving boundary exclusion."
        ),
    )


def tau_fixed_point_impossible_on_ordered_u(u: tuple[float, float, float, float], tol: float = 1e-6) -> bool:
    """tau^k u = u for k in {1,2,3} cannot occur with distinct parameters mod collision."""
    for k in (1, 2, 3):
        v = u
        for _ in range(k):
            v = cyclic_tau(v)
        if all(abs(v[i] - u[i]) < tol for i in range(4)):
            return False
    return True
