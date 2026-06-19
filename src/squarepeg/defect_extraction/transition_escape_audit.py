"""Noncompactness audit on geometric neutral transition records (Directive 052)."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state, compute_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator
from squarepeg.defect_extraction.signature_budget import audit_signature_budget

EscapeLabel = Literal[
    "SCALE_RATIO_ESCAPE",
    "CHILD_COUNT_ESCAPE",
    "CENTER_DRIFT_ESCAPE",
    "GATE_COMPLEXITY_ESCAPE",
    "WEDGE_RESERVE_ESCAPE",
    "RETAINED_RESERVE_ESCAPE",
    "SIGN_IMBALANCE_ESCAPE",
    "CROSSCUT_ESCAPE",
    "BOUNDARY_RESERVE_ESCAPE",
    "NORMALIZATION_DENOMINATOR_COLLAPSE",
    "NONE",
]

IntrinsicClass = Literal["INTRINSIC", "REMOVABLE_COBOUNDARY", "REMOVABLE_RESCALE", "ROUTED_BRANCH"]


@dataclass
class GeometricTransitionRecord:
    parent_id: str
    child_id: str
    parent_diameter: float
    child_diameter: float
    scale_ratio: float
    child_count: int
    gate_count: int
    center_offset: float
    wedge_total: float
    retained: float
    sign_imbalance: float
    crosscut: float
    Phi: float
    X: tuple[float, float, float, float, float, float, float]
    E: tuple[float, float, float, float, float, float, float]
    escape_labels: list[EscapeLabel]
    intrinsic: IntrinsicClass
    route: str


@dataclass
class TransitionEscapeAudit:
    records: list[GeometricTransitionRecord]
    family_compact: bool
    witness_parent: str | None
    witness_label: EscapeLabel | None
    messages: list[str]


def _classify_escape(
    tree: CanonicalIntrusionTree,
    parent_id: str,
    child_id: str,
    ratio: float,
    state,
    t091,
) -> tuple[list[EscapeLabel], IntrinsicClass, str]:
    labels: list[EscapeLabel] = []
    node = tree.nodes[parent_id]
    cc = len(node.child_ids)
    if t091.mu_plus_positive:
        labels.append("SCALE_RATIO_ESCAPE")
        return labels, "ROUTED_BRANCH", "POSITIVE_SCALE_END_RAY"
    if ratio < 0.05 or ratio > 0.95:
        labels.append("SCALE_RATIO_ESCAPE")
    if cc > 4:
        labels.append("CHILD_COUNT_ESCAPE")
    if state.G > 2.0 * state.Phi:
        labels.append("GATE_COMPLEXITY_ESCAPE")
    if state.R > 0.5 * state.Phi:
        labels.append("RETAINED_RESERVE_ESCAPE")
    if state.S > 0.3 * state.Phi:
        labels.append("SIGN_IMBALANCE_ESCAPE")
    if state.Phi <= 1e-12:
        labels.append("NORMALIZATION_DENOMINATOR_COLLAPSE")
    intrinsic: IntrinsicClass = "INTRINSIC" if labels else "REMOVABLE_RESCALE"
    route = "COMPACT_CORE_CANDIDATE" if not labels else "PENDING_ROUTE"
    if "SCALE_RATIO_ESCAPE" in labels and ratio < 0.05:
        intrinsic, route = "ROUTED_BRANCH", "CONCENTRATION"
    elif "CHILD_COUNT_ESCAPE" in labels:
        intrinsic, route = "ROUTED_BRANCH", "T081I_COUNTABLE_BRANCHING"
    return labels or ["NONE"], intrinsic, route


def audit_transition_escape(tree: CanonicalIntrusionTree) -> TransitionEscapeAudit:
    t091 = certify_t091(tree)
    transfer = audit_neutral_transfer_operator(tree)
    budget = audit_signature_budget(tree)
    budget_map = {b.node_id: b for b in budget.records}
    states = audit_augmented_neutral_state(tree)
    state_map = {s.node_id: s for s in states.states}
    records: list[GeometricTransitionRecord] = []
    witness: str | None = None
    witness_label: EscapeLabel | None = None
    for tr in transfer.transfers:
        if tr.parent_id not in state_map:
            continue
        st = state_map[tr.parent_id]
        node = tree.nodes[tr.parent_id]
        child = tree.nodes.get(tr.child_id)
        labels, intrinsic, route = _classify_escape(tree, tr.parent_id, tr.child_id, tr.scale_ratio, st, t091)
        br = budget_map.get(tr.parent_id)
        rec = GeometricTransitionRecord(
            tr.parent_id,
            tr.child_id,
            node.diameter,
            child.diameter if child else 0.0,
            tr.scale_ratio,
            len(node.child_ids),
            node.gate_count,
            abs(node.center[0] - (child.center[0] if child else 0.0)),
            (br.wedge_child_child + br.wedge_parent_child) if br else 0.0,
            br.retained_skeleton if br else 0.0,
            st.S,
            br.crosscut_area if br else 0.0,
            st.Phi,
            (st.Phi, st.R, st.S, st.J, st.C, st.B, st.G),
            tr.E_local,
            labels,
            intrinsic,
            route,
        )
        records.append(rec)
        if intrinsic == "INTRINSIC" and witness is None and labels != ["NONE"]:
            witness = tr.parent_id
            witness_label = labels[0]
        if t091.mu_plus_positive and witness is None:
            witness = tr.parent_id
            witness_label = "SCALE_RATIO_ESCAPE"
    compact = not any(r.intrinsic == "INTRINSIC" for r in records) and bool(records)
    if t091.mu_plus_positive:
        compact = False
    return TransitionEscapeAudit(
        records=records,
        family_compact=compact,
        witness_parent=witness,
        witness_label=witness_label,
        messages=[f"records={len(records)}, compact={compact}, witness={witness}"],
    )


def serialize_escape_fixture(tree: CanonicalIntrusionTree) -> dict:
    audit = audit_transition_escape(tree)
    return {
        "source": "directive_051_noncompact_witness",
        "family_compact": audit.family_compact,
        "witness_parent": audit.witness_parent,
        "witness_label": audit.witness_label,
        "transitions": [asdict(r) for r in audit.records[:20]],
    }
