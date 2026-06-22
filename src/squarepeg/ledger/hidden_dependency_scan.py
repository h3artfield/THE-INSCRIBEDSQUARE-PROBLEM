"""Hidden dependency scan (Directive 058)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from squarepeg.ledger.theorem_dependency_graph import build_theorem_dependency_graph

MANIFEST_057 = Path(__file__).resolve().parents[3] / "artifacts" / "directive_057_verified_internal_manifest.json"

UNIVERSAL_CLAIMS = ("T101-U", "T102-U", "T103", "T089E", "T108")


@dataclass
class HiddenDependency:
    theorem_id: str
    issue: str
    severity: str
    detail: str


@dataclass
class HiddenDependencyScan:
    findings: list[HiddenDependency]
    clean: bool
    messages: list[str]


def scan_hidden_dependencies() -> HiddenDependencyScan:
    graph = build_theorem_dependency_graph()
    scope = ""
    if MANIFEST_057.exists():
        scope = json.loads(MANIFEST_057.read_text(encoding="utf-8")).get("scope", "")
    findings: list[HiddenDependency] = []
    for tid in UNIVERSAL_CLAIMS:
        node = graph.nodes.get(tid)
        if not node:
            findings.append(HiddenDependency(tid, "MISSING_NODE", "HIGH", "not in graph"))
            continue
        if "PROVED" in node.status and "FIXTURE" in scope.upper():
            if node.scope != "FIXTURE_LOCAL" and tid != "T045R":
                findings.append(
                    HiddenDependency(
                        tid,
                        "UNSCOPED_UNIVERSAL_CLAIM",
                        "MEDIUM",
                        f"status={node.status} but manifest scope is fixture-local",
                    )
                )
    t045 = graph.nodes.get("T045R")
    if t045 and "CONJECTURAL" not in t045.status:
        findings.append(HiddenDependency("T045R", "PREMATURE_PROOF", "CRITICAL", t045.status))
    dep_flaws = [f for f in findings if f.severity == "CRITICAL"]
    return HiddenDependencyScan(
        findings=findings,
        clean=not dep_flaws,
        messages=[f"findings={len(findings)}"],
    )
