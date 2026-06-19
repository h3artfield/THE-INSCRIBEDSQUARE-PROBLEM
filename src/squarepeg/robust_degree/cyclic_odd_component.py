"""Cyclic-odd protected rhombus component definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.robust_degree.quotient_continuation import audit_quotient_continuation
from squarepeg.robust_degree.relative_rhombus_class import certify_relative_class
from squarepeg.robust_degree.twisted_w1 import audit_twisted_w1

ComponentStatus = Literal[
    "CYCLIC_ODD_CERTIFIED",
    "EULER_OBSTRUCTION_CERTIFIED",
    "UNPROTECTED",
    "ASSIGNMENT_ARTIFACT",
    "UNRESOLVED",
]


@dataclass
class CyclicOddComponent:
    name: str
    relative_class_mod2: int
    w1_pairing: int
    collision_margin: float
    side_margin: float
    rhombus_boundary_margin: float
    certified: bool
    messages: list[str] = field(default_factory=list)


def circle_cyclic_odd_component(eta: float = 0.01) -> CyclicOddComponent:
    rel = certify_relative_class(eta)
    w1 = audit_twisted_w1()
    q = audit_quotient_continuation()
    certified = (
        rel.mod2_degree == 1
        and rel.homotopy_invariant
        and w1.w1_pairing_mod2 == 1
        and q.quotient_class_nonzero
    )
    return CyclicOddComponent(
        name="unit_circle_ordered",
        relative_class_mod2=rel.mod2_degree,
        w1_pairing=w1.w1_pairing_mod2,
        collision_margin=0.1,
        side_margin=0.5,
        rhombus_boundary_margin=rel.boundary_margin,
        certified=certified,
        messages=[
            "Does not assume zero set is a manifold for arbitrary continuous gamma",
            "Uses relative Z_2 class + sign line pairing",
        ],
    )


def component_definition_text() -> str:
    return (
        "Cyclic-odd protected rhombus component: nonzero [R] in H_1(U,partial_nu U;Z_2), "
        "tau-invariant, nonzero [R_bar], sign line L_chi, <w_1(L_chi),[R_bar]>=1, "
        "positive collision/side/rhombus-boundary margins."
    )
