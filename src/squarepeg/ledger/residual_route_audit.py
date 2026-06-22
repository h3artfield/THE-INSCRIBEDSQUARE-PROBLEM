"""Residual route audit from T108/T103/T089E (Directive 058)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.ledger.residual_ledger import GLOBAL_RESIDUALS, REMOVED_RESIDUALS, build_residual_ledger

SOLVED_DESTINATIONS = (
    "T081I",
    "T068I",
    "T073",
    "T073I",
    "T064",
    "T062",
    "T080",
    "T081",
    "T087",
    "T093",
    "T091",
)


@dataclass
class RouteTrace:
    source: str
    route_label: str
    destination: str
    residual_or_solved: str
    valid: bool


@dataclass
class ResidualRouteAudit:
    traces: list[RouteTrace]
    all_routed: bool
    no_hidden_neutral: bool
    messages: list[str]


_ROUTE_MAP: list[tuple[str, str, str, str]] = [
    ("T108", "R_SUMMABLE_CHILD", "T081I", "SOLVED"),
    ("T108", "R_POSITIVE_SCALE", "T091", "SOLVED"),
    ("T108", "R_INFINITE_CENTER", "INFINITE_CENTER_GEOMETRY", "INFINITE_CENTER_GEOMETRY"),
    ("T108", "R_PARAMETER_DISCONNECTED", "PARAMETER_DISCONNECTED_LIMIT", "PARAMETER_DISCONNECTED_LIMIT"),
    ("T108", "R_COLLISION_DEGENERATION", "NON_JORDAN_SATURATION_HULL", "NON_JORDAN_SATURATION_HULL"),
    ("T103", "R_POSITIVE_SCALE", "T091", "SOLVED"),
    ("T103", "COHERENT_SOLVED_ROUTE", "T091", "SOLVED"),
    ("T089E", "NEUTRAL_CORE", "REMOVED", "NONCARLESON_SINGLETON_CANTOR_END_TANGENT"),
    ("T108", "diffuse_order", "T077-A", "NONSUMMABLE_DIFFUSE_END_GEOMETRY"),
    ("T091", "positive_scale", "annular", "POSITIVE_SCALE_NONANNULAR_CLUSTER"),
]


def audit_residual_routes() -> ResidualRouteAudit:
    ledger = build_residual_ledger()
    known = set(GLOBAL_RESIDUALS) | set(REMOVED_RESIDUALS) | set(SOLVED_DESTINATIONS) | {"SOLVED", "REMOVED"}
    traces: list[RouteTrace] = []
    for src, route, dest, residual in _ROUTE_MAP:
        valid = residual in known or dest in known
        traces.append(RouteTrace(src, route, dest, residual, valid))
    all_r = all(t.valid for t in traces)
    removed = any(r.name == "NONCARLESON_SINGLETON_CANTOR_END_TANGENT" for r in ledger.records if r.classification == "REMOVED_AS_INDEPENDENT")
    return ResidualRouteAudit(
        traces=traces,
        all_routed=all_r,
        no_hidden_neutral=removed,
        messages=[f"traces={len(traces)}, removed_singleton={removed}"],
    )
