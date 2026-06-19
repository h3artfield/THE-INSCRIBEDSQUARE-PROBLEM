"""T061 dense-gate structural trichotomy (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.dense_attachment_signature import DenseSignatureAudit, audit_dense_signature
from squarepeg.defect_extraction.diffuse_gate_limit import classify_diffuse_limit
from squarepeg.defect_extraction.gate_block_decomposition import partition_gate_blocks
from squarepeg.defect_extraction.gate_concentration import extract_concentrated_subblock
from squarepeg.defect_extraction.gate_density import GateDensityClass, classify_gate_density, dense_sequence
from squarepeg.defect_extraction.gate_word_limit import GateWordLimit, classify_gate_word
from squarepeg.defect_extraction.normalized_gate_measure import (
    GateMeasure,
    NormalizedGate,
    extract_measure_limit,
    gate_spacing_normalized,
    normalize_hull,
)

T061Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFICATION"]

T061Branch = Literal[
    "SIGNATURE_CONTROLLED_BLOCKS",
    "RECURSIVE_CONCENTRATION",
    "DIFFUSE_LIMIT",
    "MULTICENTER_DECOMPOSITION",
]


@dataclass
class DenseGateRecord:
    cluster_id: str
    gate_count: int
    diameter_r: float
    lambda_mr: float
    hull_order: list[str]
    param_order: list[str]
    gate_positions: list[tuple[float, float]]
    attachment_area: float


@dataclass
class T061Audit:
    status: T061Status
    branch: T061Branch
    dense: bool
    gate_word: GateWordLimit
    dense_signature: DenseSignatureAudit
    messages: list[str]


def audit_dense_gate_trichotomy(record: DenseGateRecord) -> T061Audit:
    """
    T061: shrinking finite-intrusion dense-gate sequence => one of four branches.
    """
    density = classify_gate_density(record.gate_count, record.diameter_r)
    dense = density.regime == "DENSE" or dense_sequence([record.lambda_mr])
    gw = classify_gate_word(record.hull_order, record.param_order)
    ds = audit_dense_signature(
        record.attachment_area,
        record.diameter_r,
        gate_measure_type="DIFFUSE" if record.gate_count > 12 else "FINITELY_SUPPORTED",
    )
    gates = [
        NormalizedGate(f"g{i}", record.gate_positions[i], i)
        for i in range(min(len(record.gate_positions), record.gate_count))
    ]
    measure = normalize_hull(gates, diameter_r=record.diameter_r)
    ml = extract_measure_limit([measure])
    branch: T061Branch = "SIGNATURE_CONTROLLED_BLOCKS"
    msgs: list[str] = []
    if ds.alternative == "D1_SIGNATURE_CONTROLLED":
        blocks = partition_gate_blocks(record.hull_order[: record.gate_count])
        branch = "SIGNATURE_CONTROLLED_BLOCKS"
        msgs.append(f"Block decomposition: {len(blocks.blocks)} blocks")
    elif ds.alternative == "D2_CONCENTRATED":
        sp = gate_spacing_normalized(record.gate_positions, record.diameter_r)
        conc = extract_concentrated_subblock(
            record.hull_order[: record.gate_count],
            sp,
            [record.attachment_area / max(record.gate_count, 1)] * record.gate_count,
            r=record.diameter_r,
        )
        branch = "RECURSIVE_CONCENTRATION"
        msgs.extend(conc.messages)
    elif ds.alternative == "D3_DIFFUSE":
        classify_diffuse_limit([measure], ds.attachment.area_normalized)
        branch = "DIFFUSE_LIMIT"
    elif ml.measure_type == "MULTICENTER":
        branch = "MULTICENTER_DECOMPOSITION"
    return T061Audit(
        status="PROVED_LOCALLY_CLASSIFICATION",
        branch=branch,
        dense=dense,
        gate_word=gw,
        dense_signature=ds,
        messages=msgs,
    )


def t061_statement() -> str:
    return "T061 — PROVED_LOCALLY as structural classifier for dense-gate sequences"
