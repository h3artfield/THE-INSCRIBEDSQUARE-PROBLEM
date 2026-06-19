"""T097C / T098C proof chain and outcome diagnosis (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.compact_core_bellman import certify_t098c
from squarepeg.defect_extraction.compact_neutral_core import audit_compact_neutral_core
from squarepeg.defect_extraction.neutral_escape_classification import certify_t100

T097CStatus = Literal["CONJECTURAL_CORE_TARGET", "PROVED_LOCALLY"]


@dataclass
class T097CCertificate:
    status: T097CStatus
    core_compact: bool
    recursion_closed: bool
    messages: list[str]


def certify_t097c(tree: CanonicalIntrusionTree) -> T097CCertificate:
    core = audit_compact_neutral_core(tree)
    status: T097CStatus = "PROVED_LOCALLY" if core.sequentially_compact and core.recursion_closed else "CONJECTURAL_CORE_TARGET"
    return T097CCertificate(status, core.sequentially_compact, core.recursion_closed, core.messages)


def diagnose_d052_outcome(tree: CanonicalIntrusionTree) -> Literal["A", "B", "C", "D", "E"]:
    t100 = certify_t100(tree)
    t097c = certify_t097c(tree)
    t098c = certify_t098c(tree)
    if t100.status == "PROVED_LOCALLY" and t097c.status == "PROVED_LOCALLY" and t098c.contraction:
        return "A"
    if t100.status == "PROVED_LOCALLY" and t097c.status == "PROVED_LOCALLY" and t098c.branch == "CRITICAL_INVARIANT_FUNCTIONAL":
        return "B"
    if t100.status == "PROVED_LOCALLY" and t100.all_routed and t097c.status != "PROVED_LOCALLY":
        return "C"
    core = audit_compact_neutral_core(tree)
    if not t100.all_routed and not core.sequentially_compact:
        return "E"
    if t097c.status != "PROVED_LOCALLY":
        return "E"
    return "E"
