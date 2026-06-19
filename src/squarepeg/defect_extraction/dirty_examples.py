"""Dirty-lobe saturation examples (Directive 028)."""

from __future__ import annotations

from squarepeg.defect_extraction.cluster_crosscut import apply_cluster_surgery, prove_cluster_crosscut_exists
from squarepeg.defect_extraction.finite_intrusion_tree import classify_finite_intrusion_tree
from squarepeg.defect_extraction.intrusion_noncrossing import IntrusionComponent
from squarepeg.defect_extraction.saturation import recursive_saturation
from squarepeg.defect_extraction.saturation_hull import saturation_hull
from squarepeg.defect_extraction.two_gate_cluster import SaturatedCluster, audit_two_gate_cluster
from squarepeg.defect_surgery.examples import example_bump_polygon


def dirty_lobe_intrusions() -> list[IntrusionComponent]:
    """Single intrusion into bump lobe Jordan domain."""
    return [
        IntrusionComponent(
            component_id="K1",
            param_interval=(0.55, 0.72),
            entry=(1.2, 0.1),
            exit=(1.8, 0.1),
            via_chord_entry=False,
            via_chord_exit=False,
            children=[],
        )
    ]


def example_dirty_saturatable_two_gate() -> tuple[list[tuple[float, float]], SaturatedCluster, bool]:
    """
    Dirty initial lobe; saturation absorbs intrusion; two-gate clean; surgery removes defects.
    """
    verts = example_bump_polygon()
    lobe_interval = (0.15, 0.45)
    lobe_boundary = [(1.0, 0.0), (1.5, 0.35), (2.0, 0.0)]
    intrusions = dirty_lobe_intrusions()
    sat = recursive_saturation(lobe_interval, intrusions)
    pts = [p for k in intrusions for p in (k.entry, k.exit)]
    hull = saturation_hull(lobe_boundary, pts)
    cluster = SaturatedCluster(
        cluster_id="dirty_L",
        saturation=sat,
        hull=hull,
        gate_a=(1.0, 0.0),
        gate_b=(2.0, 0.0),
        intrusion_depth=1,
        branching=1,
    )
    retained = [(0, 0), (3, 0), (3, 3), (0, 3), (1.0, 0.0), (2.0, 0.0)]
    audit = audit_two_gate_cluster(cluster, retained, diam_threshold=2.0)
    crosscut_ok = prove_cluster_crosscut_exists(cluster)
    return verts, cluster, audit.two_gate_clean and crosscut_ok


def certify_t053_finite_intrusion(*, all_finite_two_gate: bool) -> dict:
    """T053 — finite intrusion extraction (conjectural target)."""
    return {
        "theorem": "T053",
        "status": "CONJECTURAL_TARGET" if not all_finite_two_gate else "PROVED_LOCALLY_FINITE_INTRUSION",
        "statement": "Dominant dirty lobes with finite two-gate saturation => protected-or-surgery framework",
    }
