"""Twisted-section zero lemma for w_1 obstructions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TwistedSectionZeroLemma:
    statement: str
    proof_sketch: str
    applies_to_Mobius_over_S1: bool


def twisted_section_zero_lemma() -> TwistedSectionZeroLemma:
    return TwistedSectionZeroLemma(
        statement=(
            "Let L -> X be a real line bundle and [c] in H_1(X; Z_2). If "
            "<w_1(L), [c]> = 1, then every continuous section of L has a zero on "
            "the support of any 1-cycle representing [c]."
        ),
        proof_sketch=(
            "A nowhere-vanishing section s gives a trivialization of L over the support "
            "of c, hence <w_1(L), [c]> = 0. Contradiction."
        ),
        applies_to_Mobius_over_S1=True,
    )


def mobius_section_must_zero() -> bool:
    """S^1 with w_1=1: no global nonvanishing section."""
    return True


def diagonal_section_contradiction() -> str:
    return (
        "If D_bar is nowhere zero on R_bar supporting [Z_bar]_2, then D_bar trivializes "
        "L_chi|_{support}, forcing <w_1(L_chi), [Z_bar]_2> = 0, contradicting pairing 1."
    )
