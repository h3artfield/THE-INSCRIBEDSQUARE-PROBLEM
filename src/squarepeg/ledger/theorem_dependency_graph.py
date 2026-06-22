"""Theorem dependency graph D001–D057 (Directive 058)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

LEDGER_PATH = Path(__file__).resolve().parents[3] / "docs" / "theorem_ledger.md"

# Core closure chain (D042–D057 neutral transition arc)
CLOSURE_CHAIN: list[tuple[str, str]] = [
    ("T101-F", "T102-F"),
    ("T104", "T108"),
    ("T105R", "T108"),
    ("T106", "T108"),
    ("T107", "T105R"),
    ("T108", "T101-U"),
    ("T101-U", "T102-U"),
    ("T109", "T103"),
    ("T110", "T103"),
    ("T111", "T103"),
    ("T103", "T089E"),
    ("T108", "T089E"),
    ("T102-U", "T089E"),
    ("T089E", "T045R"),
    ("T091", "T108"),
    ("T093", "T103"),
    ("T087", "T089E"),
]

BRIDGE_EDGES: list[tuple[str, str]] = [
    ("T045", "T045R"),
    ("T043R", "T045R"),
    ("T091", "POSITIVE_SCALE_NONANNULAR_CLUSTER"),
    ("T064", "T045R"),
    ("T062", "T045R"),
    ("T081I", "T045R"),
    ("T068I", "T045R"),
    ("T073", "T045R"),
    ("T073I", "T045R"),
]


@dataclass
class TheoremNode:
    theorem_id: str
    status: str
    scope: str
    directive: str | None = None


@dataclass
class DependencyGraph:
    nodes: dict[str, TheoremNode]
    edges: list[tuple[str, str]]
    messages: list[str] = field(default_factory=list)


def _parse_ledger_statuses() -> dict[str, str]:
    text = LEDGER_PATH.read_text(encoding="utf-8") if LEDGER_PATH.exists() else ""
    out: dict[str, str] = {}
    current: str | None = None
    for line in text.splitlines():
        m = re.match(r"^## (T\d+[A-Z]?-?[A-Z]?|T\d+\*)", line)
        if m:
            current = m.group(1).replace("*", "")
        if current and line.startswith("**Status.**"):
            out[current] = line.replace("**Status.**", "").strip()
    return out


def _scope_from_status(status: str) -> str:
    s = status.upper()
    if "PROVED_LOCALLY" in s or "FIXTURE" in s or "FINITE_DOMAIN" in s:
        return "FIXTURE_LOCAL"
    if "CONJECTURAL" in s:
        return "CONJECTURAL"
    if "PROVED" in s or "VERIFIED" in s:
        return "UNIVERSAL_OR_PARTIAL"
    return "UNSCOPED"


def build_theorem_dependency_graph() -> DependencyGraph:
    statuses = _parse_ledger_statuses()
    manifest_status = {
        "T108": "PROVED_LOCALLY_CLEAN_ROOM_VERIFIED",
        "T101-U": "PROVED_LOCALLY",
        "T102-U": "PROVED_LOCALLY",
        "T103": "PROVED_LOCALLY_CLEAN_ROOM_VERIFIED",
        "T109": "PROVED_LOCALLY",
        "T110": "PROVED_LOCALLY",
        "T111": "PROVED_LOCALLY",
        "T089E": "PROVED_LOCALLY_REDUCTION",
        "T045R": "CONJECTURAL_FULL_EXTRACTION",
    }
    nodes: dict[str, TheoremNode] = {}
    for tid, st in manifest_status.items():
        nodes[tid] = TheoremNode(tid, st, "FIXTURE_LOCAL", "057")
    for tid, st in statuses.items():
        if tid not in nodes:
            nodes[tid] = TheoremNode(tid, st, _scope_from_status(st))
    edges = CLOSURE_CHAIN + BRIDGE_EDGES
    return DependencyGraph(nodes=nodes, edges=edges, messages=[f"nodes={len(nodes)}, edges={len(edges)}"])
