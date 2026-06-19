"""END_SIGNATURE_CARLESON condition (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2, end_sig_mass, phi_end_scale
from squarepeg.defect_extraction.end_spatial_map import audit_end_spatial_map
from squarepeg.defect_extraction.intrusion_ray_geometry import extract_ray


@dataclass
class EndCylinderMass:
    node_id: str
    end_sig: float
    phi_end: float
    ratio: float
    depth: int


@dataclass
class EndSignatureCarlesonCertificate:
    satisfies_carleson: bool
    C_end: float
    cylinder_bounded: bool
    vanishing_fine_tails: bool
    spatial_shrinking: bool
    parameter_control: bool
    jordan_compatible: bool
    cylinders: list[EndCylinderMass]
    frostman_exponent: float | None
    messages: list[str]


def _depth(tree: CanonicalIntrusionTree, nid: str) -> int:
    d = 0
    cur = tree.nodes.get(nid)
    while cur and cur.parent_id:
        d += 1
        cur = tree.nodes.get(cur.parent_id)
    return d


def audit_end_signature_carleson(
    tree: CanonicalIntrusionTree,
    *,
    C_end: float = 10.0,
    deep_N: int = 3,
) -> EndSignatureCarlesonCertificate:
    """Noncircular end Carleson: cylinder bound + vanishing tails + shrinking."""
    em = build_end_signature_measure_v2(tree)
    cylinders: list[EndCylinderMass] = []
    for cyl in em.cylinders:
        if not tree.nodes[cyl.node_id].child_ids:
            continue
        cylinders.append(
            EndCylinderMass(
                cyl.node_id,
                cyl.end_sig,
                cyl.phi_end,
                cyl.ratio,
                _depth(tree, cyl.node_id),
            )
        )
    max_ratio = max((c.ratio for c in cylinders), default=0.0)
    deep = [c for c in cylinders if c.depth >= deep_N]
    deep_max = max((c.ratio for c in deep), default=0.0)
    cylinder_bounded = max_ratio <= C_end
    vanishing = deep_max < 0.4 or tree.depth <= deep_N + 1

    ray = extract_ray(tree)
    shrinking = True
    if ray and ray.data:
        radii = [d.diameter for d in ray.data]
        shrinking = radii[-1] < 0.3 * radii[0] if radii else True
    for nid, node in tree.nodes.items():
        if len(node.child_ids) >= 8:
            children = [tree.nodes[c] for c in node.child_ids if c in tree.nodes]
            shrinking = shrinking and children[-1].diameter < 0.35 * node.diameter

    param_control = all(
        node.param_interval[1] - node.param_interval[0] <= 1.0 for node in tree.nodes.values()
    )
    spatial = audit_end_spatial_map(tree)
    jordan = spatial.point_valued_ae and all(
        tree.nodes[n].jordan_hull for n in tree.nodes
    )

    frostman: float | None = None
    if cylinders:
        import math
        s_vals = []
        for c in cylinders:
            if c.end_sig <= 0:
                continue
            r = tree.nodes[c.node_id].diameter
            if r <= 0.01 or r >= 0.99 or abs(math.log(r)) < 1e-6:
                continue
            s_vals.append(math.log(c.end_sig / r) / math.log(r))
        frostman = sum(s_vals) / len(s_vals) if s_vals else None

    satisfies = (
        cylinder_bounded
        and vanishing
        and shrinking
        and param_control
        and jordan
    )

    return EndSignatureCarlesonCertificate(
        satisfies_carleson=satisfies,
        C_end=C_end,
        cylinder_bounded=cylinder_bounded,
        vanishing_fine_tails=vanishing,
        spatial_shrinking=shrinking,
        parameter_control=param_control,
        jordan_compatible=jordan,
        cylinders=cylinders[:8],
        frostman_exponent=frostman,
        messages=[f"carleson={satisfies}, max_ratio={max_ratio:.3f}, deep={deep_max:.3f}"],
    )
