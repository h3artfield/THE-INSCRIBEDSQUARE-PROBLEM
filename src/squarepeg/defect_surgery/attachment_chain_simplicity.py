"""Attachment chain simplicity under gate order (Directive 026)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_surgery.annular_attachment_order import GatePair
from squarepeg.defect_surgery.exact_component_decomposition import (
    PathComponent,
    attachment_chain_vertices,
    decompose_cyclic_interval,
    master_area_identity,
)
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import Point
from squarepeg.defect_surgery.simple_signature import is_simple_polygonal_chain


@dataclass
class AttachmentChainSimplicityAudit:
    chain_points: list[Point]
    is_simple: bool
    no_retrace: bool
    matches_master_identity: bool


def build_annular_attachment_chain(components: list[PathComponent]) -> list[Point]:
    """Rebuild Z_{n,J} from component increments (same as T043R master identity)."""
    if not components:
        return []
    deltas = [c.delta for c in components]
    return attachment_chain_vertices(components[0].path[0], deltas)


def _no_segment_retrace(points: list[Point]) -> bool:
    segs = {(points[i], points[i + 1]) for i in range(len(points) - 1)}
    rev = {(b, a) for a, b in segs}
    return segs.isdisjoint(rev)


def audit_attachment_chain_simplicity(
    components: list[PathComponent],
) -> AttachmentChainSimplicityAudit:
    pts = build_annular_attachment_chain(components)
    ident = master_area_identity(components)
    simple = is_simple_polygonal_chain(pts) if len(pts) >= 3 else True
    return AttachmentChainSimplicityAudit(
        chain_points=pts,
        is_simple=simple,
        no_retrace=_no_segment_retrace(pts) if len(pts) >= 2 else True,
        matches_master_identity=ident.exact,
    )


def simplicity_under_gate_order(
    vertices: list[Point],
    forest: PacketForest,
    i0: int,
    i1: int,
    *,
    gate_ordered: bool,
) -> bool:
    """Under GATE_ORDERED + angular monotone, short-interval chain is simple."""
    decomp = decompose_cyclic_interval(vertices, i0, i1, forest)
    audit = audit_attachment_chain_simplicity(decomp.components)
    if not gate_ordered:
        return False
    return audit.is_simple and audit.matches_master_identity
