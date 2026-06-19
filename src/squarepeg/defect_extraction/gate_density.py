"""Gate density parameter Lambda = M*r (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.bounded_gate_join import C_COLLAR, q_of_m

C0 = 0.5 * C_COLLAR ** 2
C1 = 0.5 * (3 ** 2) * C_COLLAR ** 2


@dataclass
class GateComplexity:
    gate_count_m: int
    diameter_r: float
    component_q: int
    lambda_mr: float
    lambda_qr: float


@dataclass
class GateDensityClass:
    regime: Literal["SPARSE", "DENSE", "BOUNDED", "POSITIVE_SCALE"]
    lambda_value: float
    r_shrinking: bool
    messages: list[str]


def gate_complexity(m: int, r: float, q: int | None = None) -> GateComplexity:
    q_val = q if q is not None else q_of_m(m)
    return GateComplexity(
        gate_count_m=m,
        diameter_r=r,
        component_q=q_val,
        lambda_mr=m * r,
        lambda_qr=q_val * r,
    )


def join_bound_from_lambda_q(lambda_qr: float) -> float:
    """|A_join| <= C0 * Lambda_q^2 (sharp form using q r)."""
    return C0 * lambda_qr ** 2


def join_bound_from_lambda_mr(lambda_mr: float) -> float:
    """|A_join| <= C1 * Lambda^2 where Lambda = M r."""
    return C1 * lambda_mr ** 2


def join_bound_exact(q: int, r: float) -> float:
    return 0.5 * q * (q - 1) * C_COLLAR ** 2 * r ** 2


def classify_gate_density(
    m: int,
    r: float,
    *,
    sparse_threshold: float = 0.01,
    dense_threshold: float = 0.05,
    positive_scale_r: float = 0.5,
) -> GateDensityClass:
    """Sparse: M*r -> 0; Dense: limsup M*r > 0 with r->0; Positive scale: r not shrinking."""
    lam = m * r
    msgs: list[str] = []
    if r >= positive_scale_r:
        return GateDensityClass("POSITIVE_SCALE", lam, False, ["r not shrinking"])
    if lam <= sparse_threshold:
        msgs.append(f"Lambda={lam:.4f} sparse (M*r->0)")
        return GateDensityClass("SPARSE", lam, True, msgs)
    if lam >= dense_threshold:
        msgs.append(f"Lambda={lam:.4f} dense (limsup M*r>0)")
        return GateDensityClass("DENSE", lam, True, msgs)
    return GateDensityClass("BOUNDED", lam, True, ["Uniform M bound regime (T053B)"])


def sparse_sequence(lambdas: list[float], *, threshold: float = 0.01) -> bool:
    return all(l <= threshold for l in lambdas) and len(lambdas) > 0


def dense_sequence(lambdas: list[float], *, threshold: float = 0.05) -> bool:
    return max(lambdas) >= threshold if lambdas else False
