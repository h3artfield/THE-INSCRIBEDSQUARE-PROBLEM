"""T044R controlled annular surgery bridge (Directive 026)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_geometry.positive_scale_compactness import positive_scale_corollary
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import Point
from squarepeg.defect_surgery.t043r_proof import certify_t043r
from squarepeg.defect_surgery.t046_signature_theorem import T046Certificate, certify_t046

T044RStatus = Literal["PROVED_LOCALLY", "CONTROLLED_FULL_BRIDGE_TARGET", "PRECISE_GAP"]
Branch = Literal["POSITIVE_SCALE", "SHRINKING_SCALE"]


@dataclass
class T044RCertificate:
    status: T044RStatus
    branch: Branch
    positive_scale_square: bool
    shrinking_area_tight: bool
    t046: T046Certificate | None
    t043r_applies: bool
    t022_applies: bool
    messages: list[str] = field(default_factory=list)


def classify_scale_branch(diameters: list[float], *, positive_threshold: float = 0.02) -> Branch:
    if diameters and max(diameters) >= positive_threshold:
        return "POSITIVE_SCALE"
    return "SHRINKING_SCALE"


def certify_t044r(
    vertices: list[Point],
    forest: PacketForest,
    i0: int = 0,
    i1: int = 6,
    *,
    diameters: list[float] | None = None,
) -> T044RCertificate:
    ds = diameters or [d.diameter for d in forest.disks]
    branch = classify_scale_branch(ds)
    pos_square = False
    shrink_ok = False
    t046: T046Certificate | None = None
    t043r_ok = False

    if branch == "POSITIVE_SCALE":
        ps = positive_scale_corollary(ds)
        pos_square = ps.limsup_r_positive and ps.limit_square_exists
    else:
        t046 = certify_t046(vertices, forest, i0, i1)
        t043 = certify_t043r(
            forest=forest,
            beta=0.005 if t046.beta_vanishes else 0.05,
            sigma=0.005 if t046.sigma_vanishes else 0.05,
        )
        shrink_ok = t046.status == "PROVED_LOCALLY" and t043.status == "PROVED_LOCALLY"
        t043r_ok = t043.t022_applies

    status: T044RStatus = "PROVED_LOCALLY" if (
        (branch == "POSITIVE_SCALE" and pos_square) or (branch == "SHRINKING_SCALE" and shrink_ok)
    ) else "CONTROLLED_FULL_BRIDGE_TARGET"

    return T044RCertificate(
        status=status,
        branch=branch,
        positive_scale_square=pos_square,
        shrinking_area_tight=shrink_ok,
        t046=t046,
        t043r_applies=t043r_ok,
        t022_applies=t043r_ok or pos_square,
        messages=[
            "T044R dichotomy: positive scale => T036-N1-ANN square; shrinking => T046 + T043R => T022",
            f"Branch: {branch}; status: {status}",
        ],
    )


def t044r_statement() -> str:
    return (
        "T044R (PROVED_LOCALLY): ordered complete annular forest => "
        "square (positive scale) or area-tight (shrinking) => rectangular pegs."
    )
