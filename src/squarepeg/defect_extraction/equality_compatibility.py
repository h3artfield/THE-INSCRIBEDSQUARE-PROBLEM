"""Equality condition compatibility graph (Directive 049)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.equality_ledger import LedgerID, get_ledger

Compatibility = Literal["COMPATIBLE", "INCOMPATIBLE", "CONDITIONAL"]


@dataclass
class CompatibilityEdge:
    left: LedgerID
    right: LedgerID
    status: Compatibility
    reason: str


@dataclass
class EqualityCompatibilityAudit:
    edges: list[CompatibilityEdge]
    impossible_cliques: list[list[LedgerID]]
    messages: list[str]


# Known incompatible pairs: parallel (triangle) vs orthogonal (wedge) on same nonzero pair
_INCOMPATIBLE: list[tuple[LedgerID, LedgerID, str]] = [
    ("TRIANGLE_NORM", "WEDGE_PRODUCT", "same vectors cannot be parallel and orthogonal unless zero"),
    ("RETAINED_SKELETON", "CHILD_INCREMENT", "full child partition vs positive retained skeleton"),
    ("MULTIGEN_PACKING", "SIGN_GROUPING", "strict contraction vs sign-cancellation equality"),
]


def audit_equality_compatibility() -> EqualityCompatibilityAudit:
    edges: list[CompatibilityEdge] = []
    impossible: list[list[LedgerID]] = []
    ids = [e.id for e in get_ledger()]
    for a, b, reason in _INCOMPATIBLE:
        edges.append(CompatibilityEdge(a, b, "INCOMPATIBLE", reason))
        impossible.append([a, b])
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if any(e.left == a and e.right == b for e in edges):
                continue
            edges.append(CompatibilityEdge(a, b, "COMPATIBLE", "no obstruction known"))
    return EqualityCompatibilityAudit(
        edges=edges,
        impossible_cliques=impossible,
        messages=[f"edges={len(edges)}, impossible={len(impossible)}"],
    )
