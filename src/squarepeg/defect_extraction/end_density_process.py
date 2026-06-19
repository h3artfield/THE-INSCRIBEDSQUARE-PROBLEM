"""End density filtration process (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_tree_boundary import build_tree_boundary
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density


@dataclass
class EndDensityStep:
    end_id: str
    depth: int
    node_id: str
    m_v: float
    phi_v: float
    r_v: float
    D_v: float


@dataclass
class EndDensityProcessAudit:
    end_paths: list[list[EndDensityStep]]
    D_liminf: float
    D_limsup: float
    additive_mass: bool
    messages: list[str]


def _path_to_end(tree: CanonicalIntrusionTree, end_id: str) -> list[str]:
    path: list[str] = []
    cur = end_id if end_id in tree.nodes else None
    while cur:
        path.append(cur)
        cur = tree.nodes[cur].parent_id if cur in tree.nodes else None
    return list(reversed(path))


def audit_end_density_process(tree: CanonicalIntrusionTree) -> EndDensityProcessAudit:
    boundary = build_tree_boundary(tree)
    paths: list[list[EndDensityStep]] = []
    liminf_vals: list[float] = []
    limsup_vals: list[float] = []
    for end in boundary[: min(len(boundary), 32)]:
        node_path = _path_to_end(tree, end.end_id)
        steps: list[EndDensityStep] = []
        D_vals: list[float] = []
        for depth, nid in enumerate(node_path):
            if nid not in tree.nodes:
                continue
            rec = cylinder_density(tree, nid)
            steps.append(
                EndDensityStep(end.end_id, depth, nid, rec.m_v, rec.phi_v, tree.nodes[nid].diameter, rec.D_v)
            )
            if rec.phi_v > 1e-12 and rec.D_v != float("inf"):
                D_vals.append(rec.D_v)
        if steps:
            paths.append(steps)
        if D_vals:
            liminf_vals.append(min(D_vals[-3:]))
            limsup_vals.append(max(D_vals[-3:]))

    additive = True
    for nid, node in tree.nodes.items():
        if not node.child_ids:
            continue
        parent = cylinder_density(tree, nid)
        child_m = sum(cylinder_density(tree, c).m_v for c in node.child_ids if c in tree.nodes)
        if parent.m_v > 1e-9 and child_m > parent.m_v * 1.05:
            additive = False
            break

    return EndDensityProcessAudit(
        end_paths=paths,
        D_liminf=min(liminf_vals, default=0.0),
        D_limsup=max(limsup_vals, default=0.0),
        additive_mass=additive,
        messages=[f"paths={len(paths)}, additive={additive}, D_sup={max(limsup_vals, default=0):.3f}"],
    )
