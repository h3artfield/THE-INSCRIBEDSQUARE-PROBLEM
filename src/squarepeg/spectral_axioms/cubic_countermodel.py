"""Strict Model-S countermodel g_*(x) = 4x^3 - 6x^2 + 3x."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

Number = Fraction | int


def g_star(x: Number) -> Fraction:
    xf = Fraction(x)
    return 4 * xf**3 - 6 * xf**2 + 3 * xf


def g_star_centered(x: Number) -> Fraction:
    xf = Fraction(x)
    return 4 * (xf - Fraction(1, 2)) ** 3 + Fraction(1, 2)


def g_star_derivative(x: Number) -> Fraction:
    xf = Fraction(x)
    return 12 * xf**2 - 12 * xf + 3


def g_star_derivative_factored(x: Number) -> Fraction:
    xf = Fraction(x)
    return 3 * (2 * xf - 1) ** 2


def H_subadditivity(x: Number, y: Number) -> Fraction:
    """H(x,y) = g_*(x) + g_*(y) - g_*(x+y)."""
    return g_star(x) + g_star(y) - g_star(x + y)


def H_factored(x: Number, y: Number) -> Fraction:
    xf, yf = Fraction(x), Fraction(y)
    return 12 * xf * yf * (1 - xf - yf)


def D_h(x: Number, h: Number) -> Fraction:
    half = Fraction(1, 2)
    hf = Fraction(h)
    return (g_star(half + hf) - g_star(half - hf)) / (2 * hf)


def g_star_at_half_plus_h(h: Number) -> Fraction:
    hf = Fraction(h)
    return Fraction(1, 2) + 4 * hf**3


def g_star_at_half_minus_h(h: Number) -> Fraction:
    hf = Fraction(h)
    return Fraction(1, 2) - 4 * hf**3


def g_star_dual(x: Number) -> Fraction:
    """g_*(1-x) should equal 1 - g_*(x)."""
    xf = Fraction(x)
    return g_star(1 - xf)


@dataclass(frozen=True)
class CubicCountermodelFacts:
    endpoints_ok: bool
    centered_form_ok: bool
    derivative_factorization_ok: bool
    max_derivative: Fraction
    lip_constant: Fraction
    subadditivity_factorization_ok: bool
    symmetry_ok: bool
    D_h_formula_ok: bool
    kappa_threshold: Fraction


def verify_all_identities() -> CubicCountermodelFacts:
    """Direct rational verification of all polynomial identities."""
    # Endpoints
    endpoints_ok = g_star(0) == 0 and g_star(1) == 1

    # Centered form
    centered_ok = True
    for i in range(11):
        x = Fraction(i, 10)
        if g_star(x) != g_star_centered(x):
            centered_ok = False

    # Derivative factorization
    deriv_ok = True
    max_d = Fraction(0)
    for i in range(11):
        x = Fraction(i, 10)
        d1 = g_star_derivative(x)
        d2 = g_star_derivative_factored(x)
        if d1 != d2:
            deriv_ok = False
        if d1 > max_d:
            max_d = d1

    # Subadditivity factorization on sample + symbolic check points
    sub_ok = True
    test_pairs = [
        (Fraction(1, 4), Fraction(1, 3)),
        (Fraction(1, 5), Fraction(2, 5)),
        (Fraction(1, 10), Fraction(1, 10)),
        (Fraction(0), Fraction(1, 2)),
        (Fraction(1, 3), Fraction(1, 3)),
    ]
    for x, y in test_pairs:
        if x + y > 1:
            continue
        if H_subadditivity(x, y) != H_factored(x, y):
            sub_ok = False

    # Symmetry g_*(1-x) = 1 - g_*(x)
    sym_ok = True
    for i in range(11):
        x = Fraction(i, 10)
        if g_star_dual(x) != 1 - g_star(x):
            sym_ok = False

    # D_h = 4h^2
    d_h_ok = True
    for k in range(1, 10):
        h = Fraction(k, 20)
        if h >= Fraction(1, 2):
            continue
        if D_h(Fraction(1, 2), h) != 4 * h**2:
            d_h_ok = False

    return CubicCountermodelFacts(
        endpoints_ok=endpoints_ok,
        centered_form_ok=centered_ok,
        derivative_factorization_ok=deriv_ok,
        max_derivative=max_d,
        lip_constant=Fraction(3),
        subadditivity_factorization_ok=sub_ok,
        symmetry_ok=sym_ok,
        D_h_formula_ok=d_h_ok,
        kappa_threshold=Fraction(3),
    )


def strict_increase_proof_values(x: Number, y: Number) -> Fraction:
    """Integral 3(2t-1)^2 from x to y — positive for x<y."""
    xf, yf = Fraction(x), Fraction(y)
    if yf <= xf:
        raise ValueError("require x < y")
    # Antiderivative of 3(2t-1)^2 is (2t-1)^3
    return (2 * yf - 1) ** 3 - (2 * xf - 1) ** 3
