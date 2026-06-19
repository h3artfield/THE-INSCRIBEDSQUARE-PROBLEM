"""Square-mass sufficiency counterexample (Directive 024)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.attachment_chain import AttachmentChain, attachment_chain_area, mu2_on_interval

SquareMassVerdict = Literal[
    "SQUARE_MASS_SUFFICIENT",
    "SQUARE_MASS_INSUFFICIENT",
    "SUFFICIENCY_UNRESOLVED",
]

Point = tuple[float, float]


@dataclass
class SquareMassCounterexample:
    n_chords: int
    chord_diameter: float
    mu2: float
    attachment_area: float
    mu2_vanishes: bool
    attachment_persists: bool


def circle_chord_chain_counterexample(n: int = 64) -> SquareMassCounterexample:
    """
    N equal chords on unit circle: mu_2 = N * d^2 ~ N * (2pi/N)^2 = 4pi^2/N -> 0,
    but attachment chain encloses O(1) area.
    """
    if n < 8:
        n = 8
    theta = [2 * math.pi * i / n for i in range(n + 1)]
    pts = [(math.cos(t), math.sin(t)) for t in theta]
    # Chord endpoints at consecutive vertices — chain approximates circle
    chain = AttachmentChain(points=pts, chord_indices=list(range(len(pts))))
    d = 2 * math.sin(math.pi / n)  # chord length ~ 2pi/n for small
    mu2 = n * (d ** 2)
    a_att = abs(attachment_chain_area(chain))
    return SquareMassCounterexample(
        n_chords=n,
        chord_diameter=d,
        mu2=mu2,
        attachment_area=a_att,
        mu2_vanishes=mu2 < 0.5,
        attachment_persists=a_att > 0.1,
    )


def square_mass_sufficiency_verdict(n: int = 128) -> SquareMassVerdict:
    ex = circle_chord_chain_counterexample(n)
    if ex.mu2_vanishes and ex.attachment_persists:
        return "SQUARE_MASS_INSUFFICIENT"
    return "SUFFICIENCY_UNRESOLVED"


def counterexample_sequence(limit_n: int = 256) -> list[SquareMassCounterexample]:
    return [circle_chord_chain_counterexample(n) for n in [16, 32, 64, 128, limit_n]]
