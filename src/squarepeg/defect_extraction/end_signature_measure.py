"""Canonical end signature measure on cylinders (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.tree_end_cylinders import build_cylinder
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure, phi_scale


@dataclass
class CylinderEndMass:
    node_id: str
    end_sig: float
    phi_end: float
    ratio: float
    positive_mass: float
    negative_mass: float


@dataclass
class EndSignatureMeasure:
    cylinders: list[CylinderEndMass]
    total_positive: float
    total_negative: float
    total_unsigned: float
    atomic_mass: float
    continuous_mass: float
    derived_from_wedge: bool


def end_sig_mass(tree: CanonicalIntrusionTree, node_id: str) -> float:
    """mu_end([v]) from unresolved descendant signature mass."""
    sig = build_signature_measure(tree)
    mass_map = {n.node_id: n.s_local + n.edge_mass for n in sig.nodes}
    cyl = build_cylinder(tree, node_id)
    return sum(mass_map.get(e, 0.0) for e in cyl.end_ids) + mass_map.get(node_id, 0.0) * cyl.mass_fraction


def phi_end_scale(tree: CanonicalIntrusionTree, node_id: str) -> float:
    node = tree.nodes[node_id]
    return phi_scale(node)


def build_end_signature_measure_v2(tree: CanonicalIntrusionTree) -> EndSignatureMeasure:
    """Signed/unsigned end measure with atomic/continuous decomposition."""
    sig = build_signature_measure(tree)
    total = sig.total_mass or 1.0
    cylinders: list[CylinderEndMass] = []
    pos = 0.0
    neg = 0.0
    for nid, node in tree.nodes.items():
        if not node.child_ids and node.parent_id:
            continue
        es = end_sig_mass(tree, nid)
        pe = phi_end_scale(tree, nid)
        p_mass = max(es, 0.0) if node.sign >= 0 else 0.0
        n_mass = max(-es, 0.0) if node.sign < 0 else 0.0
        if node.sign >= 0 and es > 0:
            p_mass = es
        elif node.sign < 0:
            n_mass = abs(es)
        pos += p_mass
        neg += n_mass
        cylinders.append(
            CylinderEndMass(nid, es, pe, es / max(pe, 1e-9), p_mass, n_mass)
        )
    atomic = sum(c.positive_mass for c in cylinders if c.end_sig > 0 and not tree.nodes[c.node_id].child_ids)
    continuous = max(pos + neg - atomic, 0.0)
    return EndSignatureMeasure(
        cylinders=cylinders,
        total_positive=pos,
        total_negative=neg,
        total_unsigned=pos + neg,
        atomic_mass=atomic,
        continuous_mass=continuous,
        derived_from_wedge=sig.derived_from_wedge,
    )
