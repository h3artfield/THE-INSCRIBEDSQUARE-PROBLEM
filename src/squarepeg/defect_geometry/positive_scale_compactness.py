"""Positive-scale limit corollary (T036-N1-ANN-Corollary)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ScaleConclusion = Literal["FIXED_SCALE_LIMIT", "PACKET_SCALE_ONLY", "UNRESOLVED"]


@dataclass
class PositiveScaleCorollary:
    limsup_r_positive: bool
    side_bound_uniform: float
    compactness_valid: bool
    limit_square_exists: bool
    statement: str


def annular_side_bound(r_n: float, c_ann: float = 0.12) -> float:
    """Packet-scale: side(Q_n) >= c_ann * r_n."""
    return c_ann * r_n


def positive_scale_corollary(scales: list[float], c_ann: float = 0.12) -> PositiveScaleCorollary:
    """
    T036-N1-ANN-Corollary: if limsup r_n > 0, subsequence has uniform side lower bound;
    compatible convergence => limit Jordan curve has inscribed square.
    """
    if not scales:
        return PositiveScaleCorollary(
            limsup_r_positive=False,
            side_bound_uniform=0.0,
            compactness_valid=False,
            limit_square_exists=False,
            statement="No scales provided.",
        )
    limsup = max(scales[-10:]) if len(scales) >= 10 else max(scales)
    limsup_positive = limsup > 0.05
    side_lb = c_ann * limsup if limsup_positive else 0.0
    return PositiveScaleCorollary(
        limsup_r_positive=limsup_positive,
        side_bound_uniform=side_lb,
        compactness_valid=limsup_positive,
        limit_square_exists=limsup_positive,
        statement=(
            "If limsup r_n > 0 on annular-graph packets, subsequence squares have "
            f"side >= {c_ann} r_n; uniform convergence + compact U => limit square."
            if limsup_positive
            else "r_n -> 0: packet-scale only; no macroscopic limit square."
        ),
    )


def t036_n1_ann_corollary_statement() -> str:
    return (
        "T036-N1-ANN-Corollary: limsup r_n > 0 on D_nest^ann packets => subsequence with "
        "uniform side bound; limit curve contains square under compatible window convergence."
    )
