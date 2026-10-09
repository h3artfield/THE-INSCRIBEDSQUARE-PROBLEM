"""T121 — Parameter-support decomposition (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits
from squarepeg.global_geometry.parameter_support import audit_parameter_support

T121Status = Literal["CONJECTURAL_DECOMPOSITION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T121Certificate:
    status: T121Status
    decomposed: bool
    curve_level: bool
    messages: list[str]


def certify_t121(tree: CanonicalIntrusionTree) -> T121Certificate:
    support = audit_parameter_support(tree)
    limits = audit_parameter_disconnected_limits(tree)
    decomposed = limits.exhaustive and support.curve_level
    status: T121Status = "PROVED_LOCALLY" if decomposed else "CONJECTURAL_DECOMPOSITION_TARGET"
    return T121Certificate(status, decomposed, support.curve_level, limits.messages)
