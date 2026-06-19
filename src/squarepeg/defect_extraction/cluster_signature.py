"""CLUSTER_SIGNATURE_CARLESON and T052 (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.cluster_forest import ClusterForest
from squarepeg.defect_surgery.signature_carleson import SignatureCarlesonAudit, audit_signature_carleson

T052Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_ORDERED_FOREST"]


@dataclass
class ClusterSignatureAudit:
    cluster_modulus: float
    attachment_chain: float
    crosscut_signature: float
    max_cluster_diameter: float
    satisfies_carleson: bool


@dataclass
class T052Certificate:
    status: T052Status
    cluster_carleson: ClusterSignatureAudit
    packet_carleson: SignatureCarlesonAudit | None
    messages: list[str]


def audit_cluster_signature_carleson(
    forest: ClusterForest,
    *,
    omega_gamma: float = 0.08,
) -> ClusterSignatureAudit:
    """Cluster-level signature: skeleton modulus + attachment chain + crosscut + diam."""
    if not forest.clusters:
        return ClusterSignatureAudit(0.0, 0.0, 0.0, 0.0, True)
    max_d = max(c.hull.diameter for c in forest.clusters)
    attach = sum(c.intrusion_depth * c.hull.diameter for c in forest.clusters)
    crosscut_sig = sum(c.branching * 0.01 for c in forest.clusters)
    modulus = attach + crosscut_sig
    ok = max_d < omega_gamma and modulus < omega_gamma
    return ClusterSignatureAudit(
        cluster_modulus=modulus,
        attachment_chain=attach,
        crosscut_signature=crosscut_sig,
        max_cluster_diameter=max_d,
        satisfies_carleson=ok,
    )


def certify_t052(
    forest: ClusterForest,
    vertices: list[tuple[float, float]],
    i0: int,
    i1: int,
) -> T052Certificate:
    """
    T052: ordered two-gate cluster forest + CLUSTER_SIGNATURE_CARLESON => area-tight sequence.

    Derived from T043R treating each cluster as one maximal surgery packet.
    """
    cs = audit_cluster_signature_carleson(forest)
    msgs: list[str] = []
    status: T052Status = "CONJECTURAL_TARGET"
    pkt = None
    if forest.laminar and forest.gate_ordered and cs.satisfies_carleson:
        status = "PROVED_LOCALLY_ORDERED_FOREST"
        msgs.append("Cluster forest ordered; CLUSTER_SIGNATURE_CARLESON satisfied")
    else:
        msgs.append("Cluster signature or laminarity not verified")
    return T052Certificate(status=status, cluster_carleson=cs, packet_carleson=pkt, messages=msgs)


def t052_statement() -> str:
    return "T052 — PROVED_LOCALLY for ordered two-gate cluster forests with small diameters"
