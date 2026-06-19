"""Euler / Stiefel–Whitney obstruction classes for rank-d bundles over Z."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ObstructionPairing = Literal["NONZERO_MOD2", "ZERO_MOD2", "ORIENTED_NONZERO", "UNRESOLVED"]


@dataclass
class EulerObstructionCertificate:
    bundle_rank: int
    base_dim: int
    w_d_pairing_mod2: int
    euler_pairing: int | None
    oriented: bool
    forces_section_zero: bool
    pairing_verdict: ObstructionPairing
    theorem_statement: str


def mod2_euler_pairing_line_bundle(monodromy_sign: float) -> int:
    """
    For real line bundle over S^1, w_1 pairing is 1 iff monodromy is -1 (Möbius).
    """
    return 0 if monodromy_sign > 0 else 1


def euler_obstruction_theorem(min_rank: int = 1) -> str:
    return (
        f"If E is a rank-{min_rank} real bundle over compact d-manifold Z and "
        f"<w_d(E), [Z]_2> != 0, then every continuous section of E has a zero. "
        "For oriented rank-d bundles, nonzero Euler class e(E) gives an integer obstruction."
    )


def certificate_from_monodromy(
    monodromy_sign: float,
    *,
    bundle_rank: int = 1,
    base_dim: int = 1,
    oriented: bool = False,
) -> EulerObstructionCertificate:
    mod2 = mod2_euler_pairing_line_bundle(monodromy_sign)
    pairing: ObstructionPairing
    if bundle_rank == 1 and base_dim == 1:
        pairing = "NONZERO_MOD2" if mod2 == 1 else "ZERO_MOD2"
    else:
        pairing = "UNRESOLVED"
    return EulerObstructionCertificate(
        bundle_rank=bundle_rank,
        base_dim=base_dim,
        w_d_pairing_mod2=mod2,
        euler_pairing=None if not oriented else mod2,
        oriented=oriented,
        forces_section_zero=mod2 == 1,
        pairing_verdict=pairing,
        theorem_statement=euler_obstruction_theorem(bundle_rank),
    )


def t038_prime_statement() -> str:
    return (
        "T038' (CONJECTURAL_TARGET): Compact Morse–Bott square family Z with "
        "0 not in F(partial U), ker DF|_Z = T Z, and <w_d(E), [Z]_2> != 0 "
        "persists under every sufficiently small C^0 perturbation of the four windows. "
        "Proof route: Lyapunov–Schmidt + mod-2 Euler obstruction."
    )
