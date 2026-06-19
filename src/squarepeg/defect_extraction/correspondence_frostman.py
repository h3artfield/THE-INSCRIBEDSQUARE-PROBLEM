"""T090R — Correspondence Frostman criterion (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.continuum_end_reduction import certify_t091
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

T090RStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]

FrostmanComponent = Literal["SINGLETON", "CONTINUUM", "MIXED"]


@dataclass
class T090RCertificate:
    status: T090RStatus
    component: FrostmanComponent
    implies_carleson: bool
    messages: list[str]


def _spatial_cylinder_size(tree: CanonicalIntrusionTree, node_id: str) -> float:
    em = audit_endpoint_multifunction(tree)
    end_ids = {r.end_id for r in em.records}
    # descendants under node — use max Phi diameter among matching ends
    max_d = 0.0
    for r in em.records:
        if r.end_id in tree.nodes:
            cur = r.end_id
            under = False
            while cur:
                if cur == node_id:
                    under = True
                    break
                cur = tree.nodes[cur].parent_id if cur in tree.nodes else None
            if under or r.end_id == node_id:
                max_d = max(max_d, r.d_phi)
    return max(max_d, tree.nodes[node_id].diameter)


def certify_t090r(tree: CanonicalIntrusionTree) -> T090RCertificate:
    split = audit_singleton_continuum_split(tree)
    t091 = certify_t091(tree)
    carl = audit_end_signature_carleson(tree)

    comp: FrostmanComponent = "SINGLETON"
    if split.mu_plus_mass > 0.01 and split.mu_0_mass > 0.01:
        comp = "MIXED"
    elif split.mu_plus_mass > 0.01:
        comp = "CONTINUUM"

    if comp == "CONTINUUM":
        return T090RCertificate(
            status="CONJECTURAL_TARGET",
            component=comp,
            implies_carleson=False,
            messages=["continuum component routes via T091"],
        )

    implies = carl.satisfies_carleson
    status: T090RStatus = "PROVED_LOCALLY" if implies else "CONJECTURAL_TARGET"
    return T090RCertificate(
        status=status,
        component=comp,
        implies_carleson=implies,
        messages=[f"component={comp}, carleson={implies}"],
    )
