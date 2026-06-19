"""T090 — Frostman end-surgery criterion (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density

T090Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]

FrostmanClass = Literal["SUBCRITICAL", "CRITICAL", "SUPERCRITICAL"]


@dataclass
class FrostmanEndAudit:
    exponent_s: float | None
    frostman_class: FrostmanClass
    implies_carleson: bool
    messages: list[str]


@dataclass
class T090Certificate:
    status: T090Status
    frostman: FrostmanClass
    carleson: bool
    messages: list[str]


def audit_frostman_end_criterion(tree: CanonicalIntrusionTree) -> FrostmanEndAudit:
    import math
    s_vals: list[float] = []
    for nid in tree.nodes:
        rec = cylinder_density(tree, nid)
        r = tree.nodes[nid].diameter
        if rec.m_v > 1e-9 and 0.01 < r < 0.99:
            phi = rec.phi_v
            if phi > 1e-12:
                ratio = rec.m_v / phi
                if ratio > 0 and abs(math.log(r)) > 1e-6:
                    s_vals.append(math.log(ratio) / math.log(r))
    s = sum(s_vals) / len(s_vals) if s_vals else None
    fc: FrostmanClass = "CRITICAL"
    if s is not None:
        if s < 1.5:
            fc = "SUBCRITICAL"
        elif s > 2.5:
            fc = "SUPERCRITICAL"
    carl = audit_end_signature_carleson(tree)
    implies = fc == "SUBCRITICAL" or carl.satisfies_carleson
    return FrostmanEndAudit(
        exponent_s=s,
        frostman_class=fc,
        implies_carleson=implies,
        messages=[f"s={s}, class={fc}, carleson={carl.satisfies_carleson}"],
    )


def certify_t090(tree: CanonicalIntrusionTree) -> T090Certificate:
    frost = audit_frostman_end_criterion(tree)
    carl = audit_end_signature_carleson(tree)
    status: T090Status = "PROVED_LOCALLY" if frost.implies_carleson and carl.satisfies_carleson else "CONJECTURAL_TARGET"
    return T090Certificate(
        status=status,
        frostman=frost.frostman_class,
        carleson=carl.satisfies_carleson,
        messages=[f"frostman={frost.frostman_class}, carleson={carl.satisfies_carleson}"],
    )
