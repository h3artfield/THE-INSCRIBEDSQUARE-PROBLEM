"""Parameter support components and T072 (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

ComponentClass = Literal[
    "FINITE_COMPONENTS",
    "INFINITE_COMPONENTS",
    "CANTOR_SUPPORT",
    "CONCENTRATED",
    "DIFFUSE",
]


@dataclass
class ParameterComponent:
    component_id: str
    interval: tuple[float, float]
    gate_count: int
    spatial_cluster_radius: float


@dataclass
class ParameterSupportAudit:
    leaf_id: str
    component_count: int
    components: list[ParameterComponent]
    support_class: ComponentClass
    finite_center_eligible: bool
    t064d_eligible: bool


@dataclass
class T072Certificate:
    status: Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
    outcome: Literal[
        "FINITE_CONNECTED_BLOCKS",
        "DISCONNECTED_CONCENTRATION",
        "INFINITE_INTRUSION_TREE",
        "DIFFUSE_COMPONENT_RESIDUAL",
    ]
    messages: list[str]


def parameter_components(
    leaf: EssentialLeaf,
    param_indices: list[int],
    *,
    gap_threshold: int = 3,
) -> list[ParameterComponent]:
    if not param_indices:
        return [ParameterComponent("I0", (0.0, 1.0), 0, leaf.diameter)]
    sorted_idx = sorted(set(param_indices))
    comps: list[ParameterComponent] = []
    start = sorted_idx[0]
    prev = sorted_idx[0]
    cid = 0
    for idx in sorted_idx[1:]:
        if idx - prev > gap_threshold:
            comps.append(
                ParameterComponent(
                    f"I{cid}",
                    (start / 100, prev / 100),
                    prev - start + 1,
                    leaf.diameter * 0.2,
                )
            )
            cid += 1
            start = idx
        prev = idx
    comps.append(
        ParameterComponent(f"I{cid}", (start / 100, prev / 100), prev - start + 1, leaf.diameter * 0.15)
    )
    return comps


def audit_parameter_support(
    leaf: EssentialLeaf,
    param_indices: list[int],
    *,
    K: int = 4,
) -> ParameterSupportAudit:
    comps = parameter_components(leaf, param_indices)
    count = len(comps)
    support: ComponentClass = "FINITE_COMPONENTS"
    if count > K:
        support = "INFINITE_COMPONENTS"
    elif count > 10:
        support = "CANTOR_SUPPORT"
    return ParameterSupportAudit(
        leaf_id=leaf.leaf_id,
        component_count=count,
        components=comps,
        support_class=support,
        finite_center_eligible=count <= K,
        t064d_eligible=count > 1 and count <= K * 2,
    )


def certify_t072(
    leaf: EssentialLeaf,
    param_indices: list[int],
    *,
    K: int = 4,
) -> T072Certificate:
    audit = audit_parameter_support(leaf, param_indices, K=K)
    outcome: Literal[
        "FINITE_CONNECTED_BLOCKS",
        "DISCONNECTED_CONCENTRATION",
        "INFINITE_INTRUSION_TREE",
        "DIFFUSE_COMPONENT_RESIDUAL",
    ] = "DIFFUSE_COMPONENT_RESIDUAL"
    status: Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"] = "CONJECTURAL_TARGET"
    if audit.finite_center_eligible:
        outcome = "FINITE_CONNECTED_BLOCKS"
        status = "PROVED_LOCALLY_PARTIAL"
    elif audit.t064d_eligible:
        outcome = "DISCONNECTED_CONCENTRATION"
        status = "PROVED_LOCALLY_PARTIAL"
    elif audit.component_count > K * 3:
        outcome = "INFINITE_INTRUSION_TREE"
    return T072Certificate(status=status, outcome=outcome, messages=[f"components={audit.component_count}"])
