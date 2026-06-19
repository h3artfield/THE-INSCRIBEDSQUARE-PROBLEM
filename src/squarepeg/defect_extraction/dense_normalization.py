"""Dense cluster normalization (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass

Point = tuple[float, float]

ISO_DIAMETRIC = 4.0 / 3.141592653589793


@dataclass
class DenseClusterRecord:
    cluster_id: str
    diameter_r: float
    gate_count: int
    lambda_mr: float
    area_absolute: float
    center: Point


@dataclass
class NormalizedDenseCluster:
    hull_diameter: float
    area_normalized: float
    gates_normalized: list[Point]
    attachment_normalized: list[Point]
    winding_amplification: float


def normalize_dense_cluster(
    record: DenseClusterRecord,
    gate_points: list[Point],
    attachment_chain: list[Point],
) -> NormalizedDenseCluster:
    """H_tilde = (H - z_n)/r_n, diam = 1; A_Z = r^2 A_{Z_tilde}."""
    r = max(record.diameter_r, 1e-12)
    z = record.center
    gates = [((p[0] - z[0]) / r, (p[1] - z[1]) / r) for p in gate_points]
    att = [((p[0] - z[0]) / r, (p[1] - z[1]) / r) for p in attachment_chain]
    a_norm = record.area_absolute / (r * r)
    wind_amp = abs(a_norm)
    return NormalizedDenseCluster(
        hull_diameter=1.0,
        area_normalized=a_norm,
        gates_normalized=gates,
        attachment_normalized=att,
        winding_amplification=wind_amp,
    )


def is_dense_sequence(records: list[DenseClusterRecord], *, lambda_0: float = 0.05) -> bool:
    return all(rec.lambda_mr >= lambda_0 for rec in records) and all(rec.diameter_r < 0.5 for rec in records)
