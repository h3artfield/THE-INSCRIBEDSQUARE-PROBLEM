"""Tree end signature measure with exhaustion independence (Directive 043)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.diffuse_end_measure import build_end_signature_measure
from squarepeg.defect_extraction.finite_subtree_exhaustion import audit_exhaustion, build_truncation
from squarepeg.defect_extraction.intrusion_tree_ends import build_end_measure, build_end_space
from squarepeg.defect_extraction.mixed_tree_exhaustion import build_mixed_truncation
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure

EndSpatialClass = Literal[
    "SINGLE_POINT_END_CONCENTRATION",
    "FINITE_CENTER_END_MEASURE",
    "CANTOR_END_MEASURE",
    "DIFFUSE_SPATIAL_END_MEASURE",
    "NONINJECTIVE_END_MAP",
]

EndAtomSummability = Literal[
    "FINITE_ATOMIC",
    "COUNTABLY_ATOMIC_SUMMABLE",
    "COUNTABLY_ATOMIC_NONSUMMABLE",
    "NONATOMIC_DIFFUSE",
]


@dataclass
class EndSignatureRecord:
    end_id: str
    signature_mass: float
    spatial_point: tuple[float, float] | None


@dataclass
class EndMeasureIndependenceAudit:
    depth_truncation_mass: float
    mixed_truncation_mass: float
    leaf_end_mass: float
    truncation_independent: bool
    atom_class: EndAtomSummability
    spatial_class: EndSpatialClass
    end_records: list[EndSignatureRecord]
    messages: list[str]


def _classify_spatial(ends: list[EndSignatureRecord]) -> EndSpatialClass:
    pts = [e.spatial_point for e in ends if e.spatial_point]
    if not pts:
        return "NONINJECTIVE_END_MAP"
    centers = len({(round(p[0], 1), round(p[1], 1)) for p in pts})
    if centers == 1:
        return "SINGLE_POINT_END_CONCENTRATION"
    if centers <= 4:
        return "FINITE_CENTER_END_MEASURE"
    if centers > 12:
        return "CANTOR_END_MEASURE"
    return "DIFFUSE_SPATIAL_END_MEASURE"


def _classify_atoms(em, total_sig: float) -> EndAtomSummability:
    if em.measure_class == "ATOMIC":
        return "FINITE_ATOMIC"
    if em.measure_class == "COUNTABLY_ATOMIC":
        return "COUNTABLY_ATOMIC_SUMMABLE" if total_sig < 5.0 else "COUNTABLY_ATOMIC_NONSUMMABLE"
    return "NONATOMIC_DIFFUSE"


def audit_tree_end_signature_measure(tree: CanonicalIntrusionTree) -> EndMeasureIndependenceAudit:
    """Verify mu_end is independent of finite exhaustion scheme."""
    em = build_end_measure(tree)
    end_sig = build_end_signature_measure(tree)
    records = [
        EndSignatureRecord(e.end_id, e.signature_mass, e.spatial_point)
        for e in end_sig
    ]
    sig = build_signature_measure(tree)
    total_sig = sig.total_mass or 1.0

    depth_trunc = build_truncation(tree, min(3, tree.depth))
    depth_mass = sum(
        s.s_local for s in sig.nodes if s.node_id in depth_trunc.node_ids
    ) / total_sig

    mixed = build_mixed_truncation(tree, D=min(2, tree.depth), N=8)
    mixed_mass = sum(
        s.s_local for s in sig.nodes if s.node_id in mixed.node_ids
    ) / total_sig

    leaf_mass = sum(e.signature_mass for e in end_sig) / total_sig
    # Independence: leaf-end mass stable under compatible truncations
    leaf_ids = {e.end_id for e in end_sig}
    depth_leaf = sum(
        mass_map.get(n, 0.0) for n in leaf_ids if n in depth_trunc.node_ids
    ) / total_sig if (mass_map := {s.node_id: s.s_local for s in sig.nodes}) else leaf_mass
    mixed_leaf = sum(
        mass_map.get(n, 0.0) for n in leaf_ids if n in mixed.node_ids
    ) / total_sig
    independent = abs(depth_leaf - leaf_mass) < 0.05 and abs(mixed_leaf - leaf_mass) < 0.05

    return EndMeasureIndependenceAudit(
        depth_truncation_mass=depth_mass,
        mixed_truncation_mass=mixed_mass,
        leaf_end_mass=leaf_mass,
        truncation_independent=independent,
        atom_class=_classify_atoms(em, total_sig),
        spatial_class=_classify_spatial(records),
        end_records=records,
        messages=[
            f"independent={independent}, atom={_classify_atoms(em, total_sig)}, "
            f"spatial={_classify_spatial(records)}"
        ],
    )
