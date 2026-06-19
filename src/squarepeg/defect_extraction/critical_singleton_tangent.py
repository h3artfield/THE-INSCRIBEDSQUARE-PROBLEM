"""Critical singleton Cantor tangent (Directive 047)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.end_density_process import audit_end_density_process
from squarepeg.defect_extraction.finite_center_density_improvement import audit_finite_center_density_improvement
from squarepeg.defect_extraction.incidence_concentration import audit_incidence_concentration
from squarepeg.defect_extraction.noncarleson_end_density import audit_noncarleson_end_density
from squarepeg.defect_extraction.singleton_end_rigidity import audit_singleton_hypotheses
from squarepeg.defect_extraction.singleton_frostman_criterion import certify_t090r_singleton


@dataclass
class CriticalDensityCheck:
    lower_density_positive: bool
    upper_density_finite: bool
    no_frostman_gain: bool
    critical_band: bool


@dataclass
class CriticalSingletonTangentAudit:
    is_critical_residual: bool
    checks: CriticalDensityCheck
    all_singleton_hypotheses: bool
    t089r_fails: bool
    t090r_fails: bool
    messages: list[str]


def audit_critical_singleton_tangent(tree: CanonicalIntrusionTree) -> CriticalSingletonTangentAudit:
    hyp = audit_singleton_hypotheses(tree)
    nc = audit_noncarleson_end_density(tree)
    proc = audit_end_density_process(tree)
    frost = certify_t090r_singleton(tree)
    inc = audit_incidence_concentration(tree)
    imp = audit_finite_center_density_improvement(tree)
    t091 = certify_t091(tree)

    lower = proc.D_liminf > 0.05
    upper = proc.D_limsup < 50.0
    no_frost = frost.scaling_class == "CRITICAL" and not frost.implies_carleson
    critical_band = lower and upper and abs(proc.D_limsup - proc.D_liminf) < 0.5 * max(proc.D_limsup, 1e-9)

    checks = CriticalDensityCheck(lower, upper, no_frost, critical_band)
    all_hyp = (
        hyp.singleton_ae
        and hyp.shrinking_hulls
        and hyp.jordan_stable
        and hyp.parameter_connected
        and hyp.no_concentration
        and not t091.mu_plus_positive
    )
    t089_fail = nc.intrinsically_non_carleson and all_hyp and not imp.any_improvement
    t090_fail = frost.scaling_class == "CRITICAL" and not frost.implies_carleson

    is_critical = all_hyp and nc.intrinsically_non_carleson and critical_band and no_frost and t089_fail

    return CriticalSingletonTangentAudit(
        is_critical_residual=is_critical,
        checks=checks,
        all_singleton_hypotheses=all_hyp,
        t089r_fails=t089_fail,
        t090r_fails=t090_fail,
        messages=[
            f"critical={is_critical}, D=[{proc.D_liminf:.2f},{proc.D_limsup:.2f}], frost={frost.scaling_class}",
        ],
    )
