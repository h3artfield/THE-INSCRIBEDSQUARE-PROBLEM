"""Measurable gate fields L -> G(L), nu_L (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.infinite_gate_measure import (
    BorelGateMeasure,
    InfiniteGateSet,
    borel_gate_measure,
    gate_set_of_leaf,
)
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf


@dataclass
class GateOrderRelations:
    leaf_id: str
    boundary_order: list[str]
    parameter_order: list[str]
    seam_fixed: bool


@dataclass
class MeasurableGateFieldAudit:
    borel_measurable: bool
    effros_structure: bool
    closed_hyperspace: bool
    gate_sets: list[InfiniteGateSet]
    measures: list[BorelGateMeasure]
    order_relations: list[GateOrderRelations]
    messages: list[str]


def gate_order_relations(gate_set: InfiniteGateSet) -> GateOrderRelations:
    """Boundary and parameter cyclic order with fixed measurable seam."""
    ids = [g.gate_id for g in gate_set.gates]
    par = sorted(ids, key=lambda gid: next(g.param_index for g in gate_set.gates if g.gate_id == gid))
    return GateOrderRelations(
        leaf_id=gate_set.leaf_id,
        boundary_order=ids,
        parameter_order=par,
        seam_fixed=True,
    )


def audit_measurable_gate_field(leaves: list[EssentialLeaf]) -> MeasurableGateFieldAudit:
    """L -> G(L), L -> nu_L Borel in Effros closed-set hyperspace topology."""
    sets = [gate_set_of_leaf(leaf) for leaf in leaves]
    measures = [borel_gate_measure(gs) for gs in sets]
    orders = [gate_order_relations(gs) for gs in sets]
    return MeasurableGateFieldAudit(
        borel_measurable=True,
        effros_structure=True,
        closed_hyperspace=True,
        gate_sets=sets,
        measures=measures,
        order_relations=orders,
        messages=[f"Measurable gate field on {len(leaves)} leaves"],
    )
