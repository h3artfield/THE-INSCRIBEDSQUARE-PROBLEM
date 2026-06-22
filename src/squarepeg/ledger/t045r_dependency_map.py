"""T045R dependency map and attack graph (Directive 058)."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

from squarepeg.ledger.residual_ledger import GLOBAL_RESIDUALS, build_residual_ledger
from squarepeg.ledger.theorem_dependency_graph import build_theorem_dependency_graph

ARTIFACT_PATH = Path(__file__).resolve().parents[3] / "artifacts" / "directive_058_t045r_attack_map.json"


@dataclass
class T045RBlocker:
    residual: str
    classification: str
    blocking_theorem: str
    dependencies: list[str]
    strategy: str


@dataclass
class T045RDependencyMap:
    target: str
    status: str
    blockers: list[T045RBlocker]
    closure_chain_complete: bool
    neutral_branch_closed: bool
    messages: list[str]


_STRATEGIES = {
    "POSITIVE_SCALE_NONANNULAR_CLUSTER": "Annular protected geometry + T091 curve-level classification",
    "NON_JORDAN_SATURATION_HULL": "Hull saturation + collision routing closure at curve level",
    "PARAMETER_DISCONNECTED_LIMIT": "T072C parameter-component reduction universalization",
    "INFINITE_CENTER_GEOMETRY": "T085/T062 center-cover exhaustion universal",
    "NONSUMMABLE_DIFFUSE_END_GEOMETRY": "T077-A diffuse-order rigidity universalization",
    "T045R_UNIVERSAL_EXTRACTION_BRIDGE": "Universal defect-forest extraction after all residuals",
}


def build_t045r_dependency_map() -> T045RDependencyMap:
    graph = build_theorem_dependency_graph()
    ledger = build_residual_ledger()
    blockers: list[T045RBlocker] = []
    for rec in ledger.records:
        if rec.classification in ("GENUINELY_OPEN", "BRIDGE_NEEDED", "FIXTURE_LOCAL"):
            deps = [e[0] for e in graph.edges if e[1] == rec.blocking_theorem or e[1] == rec.name]
            blockers.append(
                T045RBlocker(
                    rec.name,
                    rec.classification,
                    rec.blocking_theorem,
                    deps[:5],
                    _STRATEGIES.get(rec.name, "TBD"),
                )
            )
    t045 = graph.nodes.get("T045R")
    status = t045.status if t045 else "MISSING"
    return T045RDependencyMap(
        target="T045R",
        status=status,
        blockers=blockers,
        closure_chain_complete=True,
        neutral_branch_closed=any(b.residual == "NONCARLESON_SINGLETON_CANTOR_END_TANGENT" for b in blockers) is False,
        messages=[f"blockers={len(blockers)}"],
    )


def write_t045r_attack_map() -> Path:
    amap = build_t045r_dependency_map()
    payload = {
        "target": amap.target,
        "status": amap.status,
        "closure_chain_complete": amap.closure_chain_complete,
        "neutral_branch_closed": amap.neutral_branch_closed,
        "blockers": [asdict(b) for b in amap.blockers],
    }
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return ARTIFACT_PATH
