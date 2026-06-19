"""Gate word W(C) for multi-gate saturated clusters (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

PairingKind = Literal["ADJACENT", "NESTED", "SEPARATED", "ALTERNATING", "MIXED"]


@dataclass(frozen=True)
class GateLabel:
    gate_id: str
    param_index: float
    point: tuple[float, float]


@dataclass
class GateInterval:
    """Parameter arc (g_i, g_j) inside H(C)."""

    start_gate: str
    end_gate: str
    arc_kind: Literal[
        "SATURATED_INTERNAL",
        "RETAINED_EXTERNAL",
        "HULL_BOUNDARY",
        "LOBE_CHORD",
        "SURGERY_CROSSCUT",
    ]
    param_lo: float
    param_hi: float


@dataclass
class GateWordData:
    """Gate word W(C): labels in parameter vs hull-boundary order."""

    gates: list[GateLabel]
    hull_boundary_order: list[str]
    parameter_order: list[str]
    retained_order: list[str]
    pairings: list[tuple[str, str]]
    pairing_kind: PairingKind
    seam_crossing: bool
    repeated_visits: list[str] = field(default_factory=list)


def build_gate_word(
    gates: list[GateLabel],
    *,
    hull_order: list[str] | None = None,
    param_order: list[str] | None = None,
    retained_order: list[str] | None = None,
    pairings: list[tuple[str, str]] | None = None,
) -> GateWordData:
    """Construct W(C) from gate labels and orders."""
    ids = [g.gate_id for g in gates]
    p_order = param_order or sorted(ids, key=lambda gid: next(g.param_index for g in gates if g.gate_id == gid))
    h_order = hull_order or list(reversed(p_order))
    r_order = retained_order or p_order
    pairs = pairings or _default_pairings(p_order)
    kind = classify_pairings(pairs, p_order)
    seam = any(g.param_index > 1.0 for g in gates)
    repeats = [gid for gid in ids if ids.count(gid) > 1]
    return GateWordData(
        gates=gates,
        hull_boundary_order=h_order,
        parameter_order=p_order,
        retained_order=r_order,
        pairings=pairs,
        pairing_kind=kind,
        seam_crossing=seam,
        repeated_visits=repeats,
    )


def classify_pairings(pairs: list[tuple[str, str]], param_order: list[str]) -> PairingKind:
    """Classify adjacent / nested / separated / alternating pairings."""
    if not pairs:
        return "MIXED"
    idx = {g: i for i, g in enumerate(param_order)}
    nested = separated = adjacent = 0
    for a, b in pairs:
        ia, ib = idx.get(a, 0), idx.get(b, 0)
        lo, hi = min(ia, ib), max(ia, ib)
        inside = sum(1 for g in param_order if lo < idx.get(g, -1) < hi)
        if hi - lo == 1:
            adjacent += 1
        elif inside == 0:
            separated += 1
        elif inside > 0:
            nested += 1
    if adjacent == len(pairs):
        return "ADJACENT"
    if nested == len(pairs):
        return "NESTED"
    if separated == len(pairs):
        return "SEPARATED"
    if nested and separated:
        return "ALTERNATING"
    return "MIXED"


def _default_pairings(order: list[str]) -> list[tuple[str, str]]:
    if len(order) < 2:
        return []
    pairs: list[tuple[str, str]] = []
    for i in range(0, len(order) - 1, 2):
        pairs.append((order[i], order[i + 1]))
    return pairs


def hull_vs_parameter_interleaves(word: GateWordData) -> bool:
    """True when hull and parameter cyclic orders disagree (interleaving pattern)."""
    if word.pairing_kind != "ALTERNATING":
        return False
    return word.hull_boundary_order != word.parameter_order
