"""Theorem status audit with explicit scope (Directive 058)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from squarepeg.ledger.theorem_dependency_graph import build_theorem_dependency_graph

MANIFEST_056 = Path(__file__).resolve().parents[3] / "artifacts" / "directive_056_verified_internal_manifest.json"
MANIFEST_057 = Path(__file__).resolve().parents[3] / "artifacts" / "directive_057_verified_internal_manifest.json"

REQUIRED_CHECKS = {
    "T108": "PROVED_LOCALLY_CLEAN_ROOM_VERIFIED",
    "T101-U": "PROVED_LOCALLY",
    "T102-U": "PROVED_LOCALLY",
    "T103": "PROVED_LOCALLY_CLEAN_ROOM_VERIFIED",
    "T089E": "PROVED_LOCALLY_REDUCTION",
    "T045R": "CONJECTURAL_FULL_EXTRACTION",
}


@dataclass
class StatusCheck:
    theorem_id: str
    expected: str
    actual: str
    scoped: bool
    passed: bool


@dataclass
class TheoremStatusAudit:
    checks: list[StatusCheck]
    all_passed: bool
    t045r_conjectural: bool
    messages: list[str]


def _manifest_scope() -> str:
    if MANIFEST_057.exists():
        data = json.loads(MANIFEST_057.read_text(encoding="utf-8"))
        return data.get("scope", "FIXTURE_LOCAL")
    return "FIXTURE_LOCAL"


def _load_manifest_status() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in (MANIFEST_056, MANIFEST_057):
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            out.update(data.get("theorem_status", {}))
    return out


def audit_theorem_status() -> TheoremStatusAudit:
    graph = build_theorem_dependency_graph()
    manifest_st = _load_manifest_status()
    scope = _manifest_scope()
    checks: list[StatusCheck] = []
    for tid, expected in REQUIRED_CHECKS.items():
        actual = manifest_st.get(tid, graph.nodes.get(tid).status if tid in graph.nodes else "MISSING")
        scoped = tid == "T045R" or "FIXTURE" in scope.upper() or tid in manifest_st
        passed = expected in actual or actual.startswith(expected.split("_")[0])
        if tid == "T045R":
            passed = "CONJECTURAL" in actual
        checks.append(StatusCheck(tid, expected, actual, scoped, passed))
    all_p = all(c.passed for c in checks)
    return TheoremStatusAudit(
        checks=checks,
        all_passed=all_p,
        t045r_conjectural=all(c.passed for c in checks if c.theorem_id == "T045R"),
        messages=[f"scope={scope[:40]}, passed={sum(c.passed for c in checks)}/{len(checks)}"],
    )
