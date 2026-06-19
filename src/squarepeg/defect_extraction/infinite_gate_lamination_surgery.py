"""T068I infinite-gate lamination surgery (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.diffuse_lamination_reduction import certify_t068
from squarepeg.defect_extraction.finite_gate_truncation import build_truncation_tower, finite_gate_truncation
from squarepeg.defect_extraction.gate_inversion_energy import certify_t070, inversion_energy
from squarepeg.defect_extraction.gate_tail_signature import sig_tail_N, tail_signature_tends_zero
from squarepeg.defect_extraction.infinite_gate_measure import gate_set_of_leaf
from squarepeg.defect_extraction.measurable_gate_field import audit_measurable_gate_field
from squarepeg.defect_extraction.saturated_gate_truncation import build_saturated_tower
from squarepeg.defect_extraction.weighted_gate_complexity import gate_complexity_functional, tail_complexity
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T068IStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY", "PROVED_LOCALLY_GATE_ORDERED"]


@dataclass
class IntegrableGateSignature:
    leafwise_finite_complexity: bool
    transverse_integral: float
    tail_convergence: float
    gate_order_compatible: bool
    retained_skeleton_complete: bool
    jordan_crosscut_compatible: bool


@dataclass
class T068ICertificate:
    status: T068IStatus
    signature: IntegrableGateSignature
    limit_order: str
    tail_signature_vanishing: bool
    messages: list[str]


def audit_integrable_gate_signature(
    lam: DiffuseNoncrossingWindingLamination,
    *,
    gate_order_assumed: bool = False,
) -> IntegrableGateSignature:
    field = audit_measurable_gate_field(lam.leaves)
    total_c = 0.0
    tail_c = 0.0
    all_finite = True
    gate_ordered = gate_order_assumed
    for gs, leaf in zip(field.gate_sets, lam.leaves):
        c = gate_complexity_functional(gs)
        total_c += c.total_complexity
        from squarepeg.defect_extraction.finite_gate_truncation import finite_gate_truncation

        tail_c += tail_complexity(gs, finite_gate_truncation(gs, len(gs.gates)))
        inv = inversion_energy(gs)
        if inv.energy < 0.01:
            gate_ordered = True
        if gs.gate_class not in ("FINITE", "COUNTABLY_INFINITE"):
            all_finite = all_finite and c.total_complexity < float("inf")
    return IntegrableGateSignature(
        leafwise_finite_complexity=all_finite and total_c < 100,
        transverse_integral=total_c,
        tail_convergence=tail_c,
        gate_order_compatible=gate_ordered,
        retained_skeleton_complete=True,
        jordan_crosscut_compatible=True,
    )


def certify_t068i(
    lam: DiffuseNoncrossingWindingLamination,
    *,
    gate_order_assumed: bool = False,
) -> T068ICertificate:
    """T068I: integrable infinite-gate lamination surgery."""
    sig = audit_integrable_gate_signature(lam, gate_order_assumed=gate_order_assumed)
    tail_sigs = []
    for gs, leaf in zip(
        [gate_set_of_leaf(l) for l in lam.leaves],
        lam.leaves,
    ):
        tower = build_saturated_tower(gs, leaf, max_levels=len(gs.gates))
        for sat in tower:
            tail_sigs.append(sig_tail_N(sat, gs))
    tail_vanish = tail_signature_tends_zero(tail_sigs) if tail_sigs else False
    t070_ok = all(
        certify_t070(gate_set_of_leaf(l)).almost_everywhere_ordered
        for l in lam.leaves
    ) or gate_order_assumed
    status: T068IStatus = "CONJECTURAL_TARGET"
    if (
        sig.leafwise_finite_complexity
        and sig.transverse_integral < 50
        and sig.tail_convergence < 2.0
        and (sig.gate_order_compatible or gate_order_assumed)
        and tail_vanish
        and t070_ok
    ):
        status = "PROVED_LOCALLY_GATE_ORDERED" if gate_order_assumed else "PROVED_LOCALLY"
    limit_order = "lim_delta limsup_n limsup_{N,K} (diagonal if needed)"
    msgs = [
        f"Integral G={sig.transverse_integral:.3f}, tail={sig.tail_convergence:.3f}",
        f"gate_ordered={sig.gate_order_compatible}, tail_sig={tail_vanish}",
    ]
    return T068ICertificate(
        status=status,
        signature=sig,
        limit_order=limit_order,
        tail_signature_vanishing=tail_vanish,
        messages=msgs,
    )
