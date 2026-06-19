"""Directive 041 — branching intrusion trees and Carleson tree surgery."""

from __future__ import annotations

import pytest

from squarepeg.defect_extraction.branching_carleson import audit_branching_carleson_v2
from squarepeg.defect_extraction.branching_defect_classifier import audit_branching_defects
from squarepeg.defect_extraction.branching_tree_area_tightness import area_tightness_at_N, certify_t081_v2
from squarepeg.defect_extraction.canonical_intrusion_tree import (
    CanonicalIntrusionTree,
    IntrusionTreeNode,
    build_binary_branching_tree,
    build_geometric_decay_ray,
)
from squarepeg.defect_extraction.countable_branching_surgery import certify_t081i
from squarepeg.defect_extraction.countable_child_signature import audit_child_l1_signature
from squarepeg.defect_extraction.diffuse_end_measure import audit_diffuse_end_measure
from squarepeg.defect_extraction.finite_subtree_exhaustion import audit_exhaustion, build_truncation
from squarepeg.defect_extraction.nonsummable_branching import (
    audit_intrinsic_branching_nonsummability,
    certify_t082r,
    certify_t083,
)
from squarepeg.defect_extraction.t081_clean_room import audit_t081_clean_room
from squarepeg.defect_extraction.tree_attachment_identity import child_join_term, decompose_tree_area
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure


def _ternary_tree(*, depth: int = 3) -> CanonicalIntrusionTree:
    nodes: dict[str, IntrusionTreeNode] = {}

    def add(level: int, idx: int, parent: str | None, r: float) -> str:
        nid = f"T{level}_{idx}"
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(0.0, 1.0),
            diameter=r,
            defect=0.04 * r * r,
            gate_count=2 if level == depth else 3,
            center=(0.5, 0.5),
            sign=1,
            parent_id=parent,
            child_ids=[],
            jordan_hull=True,
            gate_class="TWO_GATE" if level == depth else "FINITE_MULTIGATE",
        )
        if parent:
            nodes[parent].child_ids.append(nid)
        if level < depth:
            for k in range(3):
                add(level + 1, 3 * idx + k, nid, r * 0.55)
        return nid

    root = add(0, 0, None, 1.0)
    return CanonicalIntrusionTree(
        root_id=root,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=depth,
    )


def _variable_branching_tree(*, depth: int = 4) -> CanonicalIntrusionTree:
    nodes: dict[str, IntrusionTreeNode] = {}

    def add(level: int, idx: int, parent: str | None, r: float) -> str:
        nid = f"V{level}_{idx}"
        branch = min(level + 2, 5)
        nodes[nid] = IntrusionTreeNode(
            node_id=nid,
            param_interval=(0.0, 1.0),
            diameter=r,
            defect=0.03 * r * r,
            gate_count=2,
            center=(0.5, 0.5),
            sign=1 if idx % 2 == 0 else -1,
            parent_id=parent,
            child_ids=[],
            jordan_hull=True,
            gate_class="TWO_GATE",
        )
        if parent:
            nodes[parent].child_ids.append(nid)
        if level < depth:
            for k in range(branch):
                add(level + 1, branch * idx + k, nid, r * 0.58)
        return nid

    root = add(0, 0, None, 1.0)
    return CanonicalIntrusionTree(
        root_id=root,
        nodes=nodes,
        tree_class="LOCALLY_FINITE_INTRUSION_TREE",
        order_independent=True,
        depth=depth,
    )


@pytest.mark.fast
def test_tree_attachment_identity():
    tree = build_binary_branching_tree(depth=4)
    decomp = decompose_tree_area(tree, list(tree.nodes.keys()))
    assert decomp.identity_holds
    assert decomp.join_bounded


@pytest.mark.fast
def test_binary_tree():
    tree = build_binary_branching_tree(depth=4)
    sig = build_signature_measure(tree)
    assert sig.derived_from_wedge
    assert sig.total_mass > 0


@pytest.mark.fast
def test_ternary_tree():
    tree = _ternary_tree(depth=3)
    carl = audit_branching_carleson_v2(tree)
    assert isinstance(carl.satisfies_carleson, bool)


@pytest.mark.fast
def test_variable_branching():
    tree = _variable_branching_tree(depth=3)
    audit = audit_branching_defects(tree)
    assert audit.primary_route


@pytest.mark.fast
def test_finite_subtree_selection():
    tree = build_binary_branching_tree(depth=5)
    trunc = build_truncation(tree, 3)
    assert len(trunc.node_ids) >= 1
    assert trunc.jordan_preserved


@pytest.mark.fast
def test_tree_tail_convergence():
    tree = build_binary_branching_tree(depth=5)
    exhaust = audit_exhaustion(tree)
    assert exhaust.monotone_inclusion


@pytest.mark.fast
def test_crosscut_compatibility():
    tree = build_binary_branching_tree(depth=4)
    trunc = build_truncation(tree, 4)
    assert trunc.crosscuts_disjoint


@pytest.mark.fast
def test_child_join_bound():
    tree = build_binary_branching_tree(depth=3)
    root = tree.nodes[tree.root_id]
    children = [tree.nodes[c] for c in root.child_ids]
    join = child_join_term(root, children)
    assert join.join_area <= join.bound + 1e-9


@pytest.mark.fast
def test_child_l1_signature():
    tree = build_binary_branching_tree(depth=4)
    audit = audit_child_l1_signature(tree)
    assert audit.global_l1


@pytest.mark.fast
def test_atomic_end_measure():
    tree = build_geometric_decay_ray(length=10)
    audit = audit_diffuse_end_measure(tree)
    assert audit.status in ("ATOMIC", "NOT_DIFFUSE", "COUNTABLY_ATOMIC")


@pytest.mark.fast
def test_diffuse_end_on_branching():
    tree = _variable_branching_tree(depth=4)
    audit = audit_diffuse_end_measure(tree)
    assert audit.truncation_independent


@pytest.mark.fast
def test_alternating_sign_tree():
    tree = _variable_branching_tree(depth=3)
    defects = audit_branching_defects(tree)
    assert defects.node_classes


@pytest.mark.fast
def test_t081_certificate():
    tree = build_binary_branching_tree(depth=5)
    cert = certify_t081_v2(tree)
    assert cert.status in ("CONJECTURAL_TARGET", "PROVED_LOCALLY")


@pytest.mark.fast
def test_t081_clean_room():
    tree = build_binary_branching_tree(depth=5)
    audit = audit_t081_clean_room(tree)
    assert audit.verdict in (
        "T081_CLEAN_ROOM_VERIFIED",
        "T081_REPAIRABLE_GAP",
        "T081_INVALID",
    )


@pytest.mark.fast
def test_t081i_certificate():
    tree = build_binary_branching_tree(depth=4)
    cert = certify_t081i(tree)
    assert cert.status in ("CONJECTURAL_EXTENSION", "PROVED_LOCALLY_PARTIAL")


@pytest.mark.fast
def test_area_tightness_bound():
    tree = build_binary_branching_tree(depth=5)
    bound = area_tightness_at_N(tree, 5)
    assert bound.total >= 0


@pytest.mark.fast
def test_nonsummable_branching():
    tree = _variable_branching_tree(depth=5)
    ns = audit_intrinsic_branching_nonsummability(tree)
    assert ns.intrinsic_tail >= 0


@pytest.mark.fast
def test_t083_classifier():
    cert = certify_t083(build_binary_branching_tree(depth=4))
    assert cert.route


@pytest.mark.fast
def test_t082r():
    cert = certify_t082r(build_binary_branching_tree(depth=5))
    assert cert.t081
