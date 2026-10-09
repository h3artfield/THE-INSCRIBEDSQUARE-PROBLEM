"""T122 — Compatible component splitting (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.component_splitting import audit_component_splitting
from squarepeg.global_geometry.finite_component_parameter_split import audit_finite_component_parameter_split
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits

T122Status = Literal["CONJECTURAL_SPLITTING_TARGET", "PROVED_LOCALLY"]


@dataclass
class T122Certificate:
    status: T122Status
    splitting_valid: bool
    obstruction_preserved: bool
    messages: list[str]


def certify_t122(tree: CanonicalIntrusionTree) -> T122Certificate:
    split = audit_component_splitting(tree)
    finite = audit_finite_component_parameter_split(tree)
    limits = audit_parameter_disconnected_limits(tree)
    no_true = not any(r.true_disconnection for r in limits.records)
    valid = split.all_splittable or no_true
    obs = finite.obstruction_preserved or no_true
    status: T122Status = "PROVED_LOCALLY" if valid and obs else "CONJECTURAL_SPLITTING_TARGET"
    return T122Certificate(status, valid, obs, split.messages)
