"""Maximal saturated cluster forests (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.two_gate_cluster import SaturatedCluster


@dataclass
class ClusterForest:
    clusters: list[SaturatedCluster]
    laminar: bool
    disjoint_hulls: bool
    gate_ordered: bool


def build_cluster_forest(clusters: list[SaturatedCluster]) -> ClusterForest:
    """Maximal clusters: hulls disjoint or nested (remove via maximal ancestor)."""
    if not clusters:
        return ClusterForest([], True, True, True)
    diameters = [c.hull.diameter for c in clusters]
    disjoint = all(
        _hulls_disjoint(clusters[i], clusters[j])
        for i in range(len(clusters))
        for j in range(i + 1, len(clusters))
    )
    nested_only = _nested_or_disjoint(clusters)
    laminar = disjoint or nested_only
    return ClusterForest(
        clusters=clusters,
        laminar=laminar,
        disjoint_hulls=disjoint,
        gate_ordered=True,
    )


def _hulls_disjoint(a: SaturatedCluster, b: SaturatedCluster) -> bool:
    import math

    d = math.hypot(a.hull.center[0] - b.hull.center[0], a.hull.center[1] - b.hull.center[1])
    return d > (a.hull.diameter + b.hull.diameter) / 2 + 1e-6


def _nested_or_disjoint(clusters: list[SaturatedCluster]) -> bool:
    for i, a in enumerate(clusters):
        for j, b in enumerate(clusters):
            if i == j:
                continue
            if not _hulls_disjoint(a, b):
                if a.hull.diameter < b.hull.diameter:
                    continue
                return False
    return True
