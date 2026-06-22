"""Rank remaining global residuals for next directive (Directive 058)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.ledger.residual_ledger import build_residual_ledger

RISK_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


@dataclass
class RankedResidual:
    rank: int
    name: str
    status: str
    blocking_theorem: str
    dependencies: str
    strategy: str
    risk_level: str
    recommended_directive: int


@dataclass
class NextTargetRanking:
    ranked: list[RankedResidual]
    primary_target: str
    primary_directive: int
    multiple_equivalent: bool
    messages: list[str]


_DIRECTIVE_MAP = {
    "POSITIVE_SCALE_NONANNULAR_CLUSTER": 59,
    "NON_JORDAN_SATURATION_HULL": 60,
    "PARAMETER_DISCONNECTED_LIMIT": 61,
    "INFINITE_CENTER_GEOMETRY": 62,
    "NONSUMMABLE_DIFFUSE_END_GEOMETRY": 63,
    "T045R_UNIVERSAL_EXTRACTION_BRIDGE": 64,
}


_PATH_ORDER = [
    "POSITIVE_SCALE_NONANNULAR_CLUSTER",
    "NONSUMMABLE_DIFFUSE_END_GEOMETRY",
    "INFINITE_CENTER_GEOMETRY",
    "PARAMETER_DISCONNECTED_LIMIT",
    "NON_JORDAN_SATURATION_HULL",
    "T045R_UNIVERSAL_EXTRACTION_BRIDGE",
]


def rank_next_targets() -> NextTargetRanking:
    ledger = build_residual_ledger()
    open_records = [r for r in ledger.records if r.classification not in ("REMOVED_AS_INDEPENDENT", "SOLVED")]
    open_records.sort(key=lambda r: _PATH_ORDER.index(r.name) if r.name in _PATH_ORDER else 99)
    ranked: list[RankedResidual] = []
    for i, rec in enumerate(open_records, 1):
        ranked.append(
            RankedResidual(
                i,
                rec.name,
                rec.classification,
                rec.blocking_theorem,
                rec.route_source,
                _strategy(rec.name),
                rec.risk_level,
                _DIRECTIVE_MAP.get(rec.name, 59 + i),
            )
        )
    primary = ranked[0].name if ranked else "NONE"
    primary_d = ranked[0].recommended_directive if ranked else 59
    equiv = sum(1 for r in ranked[:2] if r.risk_level == ranked[0].risk_level) > 1 and ranked[0].name != "POSITIVE_SCALE_NONANNULAR_CLUSTER"
    return NextTargetRanking(
        ranked=ranked,
        primary_target=primary,
        primary_directive=primary_d,
        multiple_equivalent=equiv and primary != "POSITIVE_SCALE_NONANNULAR_CLUSTER",
        messages=[f"primary={primary}, d={primary_d}"],
    )


def _strategy(name: str) -> str:
    strategies = {
        "POSITIVE_SCALE_NONANNULAR_CLUSTER": "Curve-level T091 annular/nonannular split + positive-scale cluster surgery",
        "NON_JORDAN_SATURATION_HULL": "Universal hull collision saturation classification",
        "PARAMETER_DISCONNECTED_LIMIT": "Universal parameter-component disconnected limit reduction",
        "INFINITE_CENTER_GEOMETRY": "Infinite-center transition universal exhaustion",
        "NONSUMMABLE_DIFFUSE_END_GEOMETRY": "T077-A universal diffuse-order impossibility",
        "T045R_UNIVERSAL_EXTRACTION_BRIDGE": "Close universal extraction after all global residuals",
    }
    return strategies.get(name, "TBD")
