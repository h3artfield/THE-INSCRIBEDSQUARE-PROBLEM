"""End entropy and scale drift (Directive 048)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class EntropyDriftRecord:
    node_id: str
    H_v: float
    Lambda_v: float
    log_D_drift: float
    positive_scale_drift: bool


@dataclass
class EndEntropyDriftAudit:
    records: list[EntropyDriftRecord]
    avg_entropy: float
    avg_scale_drift: float
    density_drift_controlled: bool
    messages: list[str]


def audit_end_entropy_drift(tree: CanonicalIntrusionTree) -> EndEntropyDriftAudit:
    records: list[EntropyDriftRecord] = []
    entropies: list[float] = []
    drifts: list[float] = []

    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        parent = cylinder_density(tree, nid)
        masses = [cylinder_density(tree, c).m_v for c in node.child_ids if c in tree.nodes]
        total_m = sum(masses) or 1.0
        probs = [m / total_m for m in masses if m > 1e-12]
        H = -sum(p * math.log(p + 1e-15) for p in probs) if probs else 0.0
        rv = node.diameter
        lam = 0.0
        log_d = 0.0
        for c, m in zip(node.child_ids, masses):
            if c not in tree.nodes or m <= 1e-12:
                continue
            rw = tree.nodes[c].diameter
            p = m / total_m
            if rw > 1e-12 and rv > 1e-12:
                lam += p * math.log(rv / rw)
            child_d = cylinder_density(tree, c).D_v
            if parent.D_v > 1e-12 and child_d > 1e-12:
                log_d += p * (math.log(child_d) - math.log(parent.D_v))
        pos_drift = lam > 0.05
        records.append(EntropyDriftRecord(nid, H, lam, log_d, pos_drift))
        entropies.append(H)
        drifts.append(lam)

    controlled = all(abs(r.log_D_drift) < 0.5 or r.positive_scale_drift for r in records)
    return EndEntropyDriftAudit(
        records=records,
        avg_entropy=sum(entropies) / len(entropies) if entropies else 0.0,
        avg_scale_drift=sum(drifts) / len(drifts) if drifts else 0.0,
        density_drift_controlled=controlled,
        messages=[f"avg_H={sum(entropies)/max(len(entropies),1):.3f}, drift_control={controlled}"],
    )
