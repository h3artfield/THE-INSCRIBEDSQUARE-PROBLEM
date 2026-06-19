"""Interval coverage certificate for transition domain (Directive 053)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from squarepeg.defect_extraction.transition_domain_cover import audit_transition_domain_cover

DOMAIN_VERSION = "053-finite-normalized-v1"
NORMALIZATION = "Phi_parent=1 projective section"


@dataclass
class IntervalCellCert:
    cell_id: str
    ratio_interval: list[float]
    route: str
    margin: float
    destination: str
    status: str


@dataclass
class TransitionIntervalCertificate:
    domain_version: str
    normalization: str
    cells: list[IntervalCellCert]
    unresolved_cells: int
    complete: bool
    source_hash: str


def build_interval_certificate() -> TransitionIntervalCertificate:
    cover = audit_transition_domain_cover()
    cells: list[IntervalCellCert] = []
    dest_map = {
        "P_concentration": "T064_T085",
        "P_finite_center": "T062_T089R",
        "P_plateau": "T085_PLATEAU",
        "P_positive_scale": "T091",
        "P_summable_children": "T081I",
        "P_bookkeeping_coboundary": "COBOUNDARY_QUOTIENT",
    }
    for c in cover.cells:
        cells.append(
            IntervalCellCert(
                c.cell_id,
                [c.ratio_lo, c.ratio_hi],
                c.route,
                0.001,
                dest_map.get(c.route, "UNRESOLVED"),
                c.status,
            )
        )
    payload = json.dumps([asdict(x) for x in cells], sort_keys=True)
    h = hashlib.sha256(payload.encode()).hexdigest()[:16]
    return TransitionIntervalCertificate(
        DOMAIN_VERSION,
        NORMALIZATION,
        cells,
        cover.unresolved_cells,
        cover.finite_domain_covered,
        h,
    )


def write_coverage_certificate(path: Path | None = None) -> TransitionIntervalCertificate:
    cert = build_interval_certificate()
    if path is None:
        path = Path(__file__).resolve().parents[3] / "artifacts" / "universal_transition_coverage_certificate.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "domain_version": cert.domain_version,
                "normalization": cert.normalization,
                "cells": [asdict(c) for c in cert.cells],
                "unresolved_cells": cert.unresolved_cells,
                "complete": cert.complete,
                "source_hash": cert.source_hash,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return cert
