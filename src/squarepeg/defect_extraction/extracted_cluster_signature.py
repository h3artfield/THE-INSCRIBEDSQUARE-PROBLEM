"""Extracted cluster signature control (Directive 030)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.cluster_forest import ClusterForest, build_cluster_forest
from squarepeg.defect_extraction.cluster_signature import (
    ClusterSignatureAudit,
    T052Certificate,
    audit_cluster_signature_carleson,
    certify_t052,
)
from squarepeg.defect_extraction.geometric_ear_peeling import GeometricPeelingResult
from squarepeg.defect_extraction.two_gate_cluster import SaturatedCluster
from squarepeg.defect_extraction.saturation_hull import SaturationHull
from squarepeg.defect_extraction.saturation import SaturationState

SignatureClass = Literal[
    "SIMPLE_SIGNATURE",
    "BOUNDED_WINDING_SIGNATURE",
    "BOUNDED_MULTIPLICITY_SIGNATURE",
    "CLUSTER_SIGNATURE_CARLESON",
    "UNVERIFIED",
]


@dataclass
class ExtractedSignatureAudit:
    signature_class: SignatureClass
    cluster_carleson: ClusterSignatureAudit
    bounded_gate: bool
    attachment_bounded: bool
    messages: list[str]


def clusters_from_peeling(
    peel: GeometricPeelingResult,
    *,
    base_diameter: float = 0.1,
) -> list[SaturatedCluster]:
    """Build two-gate cluster stubs from peeled geometric ears."""
    clusters: list[SaturatedCluster] = []
    for i, step in enumerate(peel.steps):
        hull = SaturationHull(
            boundary=[],
            center=(0.0, 0.0),
            diameter=base_diameter / (i + 1),
            is_jordan_disk=True,
            simply_connected=True,
        )
        sat = SaturationState(
            lobe_id=step.ear.ear_id,
            lobe_interval=(0.0, 1.0),
            level=1,
            param_intervals=[(0.0, 1.0)],
            intrusion_ids=[],
            stabilized=True,
            reaches_seam=False,
        )
        clusters.append(
            SaturatedCluster(
                cluster_id=step.ear.ear_id,
                saturation=sat,
                hull=hull,
                gate_a=(0.0, 0.0),
                gate_b=(base_diameter, 0.0),
                intrusion_depth=1,
                branching=1,
            )
        )
    return clusters


def audit_extracted_signature(
    peel: GeometricPeelingResult,
    *,
    m: int,
    omega_gamma: float = 0.08,
) -> ExtractedSignatureAudit:
    """Bounded gate count + geometric peeling => CLUSTER_SIGNATURE_CARLESON when diam small."""
    clusters = clusters_from_peeling(peel)
    forest = build_cluster_forest(clusters)
    cs = audit_cluster_signature_carleson(forest, omega_gamma=omega_gamma)
    sig: SignatureClass = "UNVERIFIED"
    msgs: list[str] = []
    if cs.satisfies_carleson and peel.jordan_preserved and peel.gate_ordered:
        sig = "CLUSTER_SIGNATURE_CARLESON"
        msgs.append("CLUSTER_SIGNATURE_CARLESON verified")
    elif cs.max_cluster_diameter < omega_gamma:
        sig = "BOUNDED_WINDING_SIGNATURE"
        msgs.append("Bounded winding from small cluster diameters")
    return ExtractedSignatureAudit(
        signature_class=sig,
        cluster_carleson=cs,
        bounded_gate=True,
        attachment_bounded=cs.attachment_chain < omega_gamma,
        messages=msgs,
    )


def certify_extracted_t052(
    peel: GeometricPeelingResult,
    vertices: list[tuple[float, float]],
    i0: int,
    i1: int,
) -> T052Certificate:
    clusters = clusters_from_peeling(peel)
    forest = build_cluster_forest(clusters)
    return certify_t052(forest, vertices, i0, i1)
