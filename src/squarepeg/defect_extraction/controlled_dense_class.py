"""T062 controlled dense-gate subclasses (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.dense_attachment_signature import audit_dense_signature
from squarepeg.defect_extraction.gate_block_decomposition import partition_gate_blocks
from squarepeg.defect_extraction.gate_word_limit import asymptotically_ordered, classify_gate_word
from squarepeg.defect_extraction.normalized_gate_measure import (
    NormalizedGate,
    extract_measure_limit,
    normalize_hull,
)
from squarepeg.defect_extraction.sparse_gate_extraction import certify_t060
from squarepeg.defect_extraction.gate_graph import example_four_gate_graph

T062Status = Literal["CONTROLLED_CLASS_TARGET", "PROVED_LOCALLY_ORDERED_DIFFUSE", "PROVED_LOCALLY_FINITE_CENTER"]

ControlledClass = Literal["ORDERED_DIFFUSE_GATES", "FINITE_CENTER_DENSE_GATES"]


@dataclass
class T062Certificate:
    status: T062Status
    controlled_class: ControlledClass
    block_count: int
    center_count: int
    extraction_possible: bool
    messages: list[str]


def certify_ordered_diffuse(
    gate_ids: list[str],
    hull_order: list[str],
    param_order: list[str],
    *,
    m: int,
    r: float,
    attachment: float = 0.02,
) -> T062Certificate:
    """Ordered diffuse: asymptotically ordered => bounded winding signature."""
    gw = classify_gate_word(hull_order, param_order)
    ordered = gw.order_class == "ASYMPTOTICALLY_ORDERED"
    ds = audit_dense_signature(attachment, r, gate_measure_type="DIFFUSE")
    blocks = partition_gate_blocks(gate_ids)
    extract = ordered and ds.alternative in ("D1_SIGNATURE_CONTROLLED", "D3_DIFFUSE")
    status: T062Status = "CONTROLLED_CLASS_TARGET"
    if extract and blocks.blocks:
        status = "PROVED_LOCALLY_ORDERED_DIFFUSE"
    return T062Certificate(
        status=status,
        controlled_class="ORDERED_DIFFUSE_GATES",
        block_count=len(blocks.blocks),
        center_count=1,
        extraction_possible=extract,
        messages=["Ordered diffuse => blockwise T053B" if extract else "Open"],
    )


def certify_finite_center_dense(
    gate_positions: list[tuple[float, float]],
    gate_ids: list[str],
    *,
    k: int = 3,
    r: float = 0.08,
    attachment: float = 0.02,
) -> T062Certificate:
    """At most K center regions => blockwise T053B + cross-center join estimate."""
    gates = [NormalizedGate(gid, pos, i) for i, (gid, pos) in enumerate(zip(gate_ids, gate_positions))]
    measure = normalize_hull(gates, diameter_r=r)
    ml = extract_measure_limit([measure])
    from squarepeg.defect_extraction.normalized_gate_measure import _detect_centers

    centers = _detect_centers(measure.positions)
    blocks = partition_gate_blocks(gate_ids)
    extract = len(centers) <= k and len(blocks.blocks) <= k + 2
    status: T062Status = "CONTROLLED_CLASS_TARGET"
    if extract:
        status = "PROVED_LOCALLY_FINITE_CENTER"
    return T062Certificate(
        status=status,
        controlled_class="FINITE_CENTER_DENSE_GATES",
        block_count=len(blocks.blocks),
        center_count=len(centers),
        extraction_possible=extract,
        messages=[f"{len(centers)} centers, {len(blocks.blocks)} blocks"],
    )
