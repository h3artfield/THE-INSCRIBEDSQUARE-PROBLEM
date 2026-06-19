"""Dense-gate normalized attachment signature (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Point = tuple[float, float]

DenseAlternative = Literal["D1_SIGNATURE_CONTROLLED", "D2_CONCENTRATED", "D3_DIFFUSE", "D4_MULTICENTER"]


@dataclass
class NormalizedAttachment:
    area_absolute: float
    area_normalized: float
    diameter_r: float
    winding_lower_bound: float
    high_winding: bool


@dataclass
class DenseSignatureAudit:
    alternative: DenseAlternative
    attachment: NormalizedAttachment
    epsilon_0: float
    messages: list[str]


def normalize_attachment_chain(
    area_z: float,
    diameter_r: float,
    *,
    center: Point = (0.0, 0.0),
) -> NormalizedAttachment:
    """
    A_{Z_n} = r_n^2 * A_{Z_tilde_n}.

    Join-dominated with fixed defect requires |A_{Z_tilde}| -> infinity.
    """
    r = max(diameter_r, 1e-12)
    r2 = r * r
    a_norm = area_z / r2
    eps = 0.025
    high = abs(a_norm) > eps / r2 and r < 0.5
    wind_lb = abs(area_z) / r2 if r > 0 else 0.0
    return NormalizedAttachment(
        area_absolute=area_z,
        area_normalized=a_norm,
        diameter_r=r,
        winding_lower_bound=wind_lb,
        high_winding=high,
    )


def winding_amplification(area_z: float, diameter_r: float) -> float:
    """sup_z |wind(Z_tilde, z)| >= c * epsilon_0 / r^2 -> infinity as r->0."""
    r = max(diameter_r, 1e-12)
    return abs(area_z) / (r * r)


def audit_dense_signature(
    area_z: float,
    diameter_r: float,
    *,
    gate_measure_type: str = "DIFFUSE",
    concentrated_fraction: float = 0.0,
) -> DenseSignatureAudit:
    att = normalize_attachment_chain(area_z, diameter_r)
    alt: DenseAlternative = "D1_SIGNATURE_CONTROLLED"
    msgs: list[str] = []
    if abs(att.area_normalized) < 0.01 and not att.high_winding:
        alt = "D1_SIGNATURE_CONTROLLED"
        msgs.append("Normalized attachment vanishes — surgery applies")
    elif concentrated_fraction >= 0.25:
        alt = "D2_CONCENTRATED"
        msgs.append("Subblock carries fixed defect fraction")
    elif gate_measure_type == "DIFFUSE":
        alt = "D3_DIFFUSE"
        msgs.append("Diffuse gate limit with distributed attachment")
    elif gate_measure_type == "MULTICENTER":
        alt = "D4_MULTICENTER"
        msgs.append("Multicenter gate decomposition")
    elif att.high_winding:
        alt = "D2_CONCENTRATED"
        msgs.append("High normalized winding — concentrated regime")
    return DenseSignatureAudit(alternative=alt, attachment=att, epsilon_0=0.025, messages=msgs)
