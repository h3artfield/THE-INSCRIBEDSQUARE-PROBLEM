"""Synthetic spectral branch stress tests (diagnostic, not Floer theory)."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from squarepeg.spectral_axioms.cubic_countermodel import (
    g_star,
    g_star_derivative,
)


@dataclass
class SyntheticBranch:
    name: str
    a_prime: callable  # maps x -> a'(x) = r(x)^2
    description: str


@dataclass
class SyntheticTestResult:
    test_name: str
    can_represent_g_star: bool | None  # None = inconclusive
    reason: str
    assumptions: list[str] = field(default_factory=list)


def single_branch_g_from_a_prime(a_prime: callable, samples: int = 50) -> list[tuple[Fraction, Fraction]]:
    """g(x) = ∫_0^x a'(t) dt / ∫_0^1 a'(t) dt."""
    xs = [Fraction(i, samples) for i in range(samples + 1)]
    integrals = [Fraction(0)]
    for i in range(1, samples + 1):
        x_prev, x_curr = xs[i - 1], xs[i]
        avg = (Fraction(a_prime(x_prev)) + Fraction(a_prime(x_curr))) / 2
        integrals.append(integrals[-1] + avg * (x_curr - x_prev))
    total = integrals[-1]
    return [(xs[i], integrals[i] / total) for i in range(samples + 1)]


def test_single_branch_equals_g_star() -> SyntheticTestResult:
    """Single branch with a'(x) = g_*'(x) normalizes to g_* itself."""
    def a_prime(x):
        return g_star_derivative(x)

    values = single_branch_g_from_a_prime(a_prime)
    max_err = Fraction(0)
    for x, g_val in values:
        err = abs(g_val - g_star(x))
        if err > max_err:
            max_err = err
    ok = max_err < Fraction(1, 1000)
    return SyntheticTestResult(
        test_name="single_branch_a_prime_equals_g_star_derivative",
        can_represent_g_star=ok,
        reason=f"max normalization error {max_err}; single branch CAN match g_*",
        assumptions=["one smooth branch", "a'(x)=g_*'(x)", "continuous selector"],
    )


def test_branch_duality_a_prime_symmetric() -> SyntheticTestResult:
    """
    g_*'(1-x) = g_*'(x) because (2x-1)^2 is symmetric about x=1/2.
    Symmetric branch radius is COMPATIBLE; zero at x=1/2 is the issue.
    """
    x = Fraction(1, 4)
    symmetric = g_star_derivative(1 - x) == g_star_derivative(x)
    zero_at_half = g_star_derivative(Fraction(1, 2)) == 0
    return SyntheticTestResult(
        test_name="branch_duality_a_prime_symmetric",
        can_represent_g_star=symmetric,
        reason="g_*'(1-x)=g_*'(x) — symmetric branch duality holds; radius zero at 1/2",
        assumptions=["branch duality a'(1-x)=a'(x)"],
    )


def test_positive_radius_at_midpoint() -> SyntheticTestResult:
    """Strict geometric rectangles need R>0; g_*'(1/2)=0 violates positive radius."""
    r_sq = g_star_derivative(Fraction(1, 2))
    return SyntheticTestResult(
        test_name="positive_radius_at_midpoint",
        can_represent_g_star=r_sq > 0,
        reason=f"g_*'(1/2)={r_sq} — zero formal radius at square angle",
        assumptions=["R^2 = g'(x) > 0 for genuine nondegenerate rectangles"],
    )


def test_z4_permutation_abstract() -> SyntheticTestResult:
    """Abstract Z4 on branches cannot fix asymmetric derivative without extra structure."""
    return SyntheticTestResult(
        test_name="abstract_z4_action",
        can_represent_g_star=None,
        reason="g_* lacks 4-fold symmetry in derivative; Z4 action on branches undefined at scalar level",
        assumptions=["abstract Z4 permutation on branch labels"],
    )


def run_all_synthetic_tests() -> list[SyntheticTestResult]:
    return [
        test_single_branch_equals_g_star(),
        test_branch_duality_a_prime_symmetric(),
        test_positive_radius_at_midpoint(),
        test_z4_permutation_abstract(),
    ]
