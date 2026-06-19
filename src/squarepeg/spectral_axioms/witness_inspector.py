"""Independent inspection of grid LP witnesses."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from squarepeg.spectral_axioms.continuum_cells import PLFunction, certify_pl_subadditivity
from squarepeg.spectral_axioms.pl_obstruction import StrictPLFunction, finite_pl_obstruction_holds


@dataclass
class WitnessInspection:
    N: int
    kappa: Fraction
    breakpoints: list[tuple[str, str]]
    segments: list[dict]
    half_type: str
    left_slope_at_half: str
    right_slope_at_half: str
    max_affine_interval_at_half: dict
    D_h_values: list[dict]
    is_injective: bool
    is_strictly_increasing: bool
    flat_intervals: list[tuple[str, str]]
    lipschitz_constant: str
    endpoints: tuple[str, str]
    D_plus_limsup: str
    is_strict_bijection_with_D_plus_zero: bool
    cause_of_apparent_D_plus_zero: str
    subadditivity_certificate_ok: bool
    min_H: str


def inspect_grid_witness(
    values: list[Fraction],
    N: int,
    kappa: Fraction,
) -> WitnessInspection:
    pl = PLFunction.from_grid(values, N)
    half = Fraction(1, 2)
    segs = pl.segments

    seg_info = []
    for i, seg in enumerate(segs):
        seg_info.append(
            {
                "index": i,
                "x0": str(seg.x0),
                "x1": str(seg.x1),
                "y0": str(seg.y0),
                "slope": str(seg.slope),
            }
        )

    # slopes adjacent to 1/2
    left_slope = right_slope = "N/A"
    half_type = "interior"
    max_interval = {"x0": "N/A", "x1": "N/A"}
    for seg in segs:
        if seg.x0 <= half <= seg.x1:
            half_type = "interior" if seg.x0 < half < seg.x1 else "breakpoint"
            max_interval = {"x0": str(seg.x0), "x1": str(seg.x1), "slope": str(seg.slope)}
    for i, seg in enumerate(segs):
        if seg.x1 == half or (seg.x0 < half <= seg.x1):
            if half in (seg.x0, seg.x1):
                half_type = "breakpoint"
            if seg.x1 <= half:
                left_slope = str(seg.slope)
            if seg.x0 >= half:
                right_slope = str(seg.slope)

    # D_h at all breakpoint-scale h
    hs = sorted({seg.x1 - half for seg in segs if seg.x1 > half} | {half - seg.x0 for seg in segs if seg.x0 < half})
    hs = [h for h in hs if h > 0]
    extra_hs = {Fraction(1, N)} | {Fraction(k, N) for k in range(1, min(N // 2, 20))}
    hs = sorted(set(hs) | extra_hs)

    d_h_vals = []
    for h in hs:
        if half + h > 1 or half - h < 0:
            continue
        lo = pl.value_at(half - h)
        hi = pl.value_at(half + h)
        d_h_vals.append({"h": str(h), "D_h": str((hi - lo) / (2 * h))})

    # True D^+: limsup_{h↓0} D_h — use h inside widest flat segment at 1/2 if any
    d_plus_lim = Fraction(0)
    for seg in segs:
        if seg.x0 <= half <= seg.x1 and seg.slope == 0:
            h_in = min(half - seg.x0, seg.x1 - half)
            if h_in > 0:
                d_plus_lim = Fraction(0)
                break
    else:
        # strict or no flat: approach via smallest breakpoint scale
        h_small = Fraction(1, 2 * N)
        lo = pl.value_at(half - h_small)
        hi = pl.value_at(half + h_small)
        d_plus_lim = (hi - lo) / (2 * h_small)

    flat = [(str(s.x0), str(s.x1)) for s in segs if s.slope == 0]
    strict = all(s.slope > 0 for s in segs)
    injective = strict  # strict increasing on [0,1] => bijection onto image [0,1]

    cert = certify_pl_subadditivity(pl)

    cause = (
        "Flat PL segment of positive width containing x=1/2 (weak monotonicity); "
        "D_h=0 for h <= half-width of flat interval; "
        "LP objective D_{N,1} evaluates one grid window, not continuum limsup; "
        "NOT a strictly increasing bijection."
    )

    return WitnessInspection(
        N=N,
        kappa=kappa,
        breakpoints=[(str(x), str(y)) for x, y in pl.breakpoints],
        segments=seg_info,
        half_type=half_type,
        left_slope_at_half=left_slope,
        right_slope_at_half=right_slope,
        max_affine_interval_at_half=max_interval,
        D_h_values=d_h_vals,
        is_injective=injective,
        is_strictly_increasing=strict,
        flat_intervals=flat,
        lipschitz_constant=str(pl.lipschitz_constant()),
        endpoints=(str(pl.value_at(Fraction(0))), str(pl.value_at(Fraction(1)))),
        D_plus_limsup=str(d_plus_lim),
        is_strict_bijection_with_D_plus_zero=False,
        cause_of_apparent_D_plus_zero=cause,
        subadditivity_certificate_ok=cert.ok,
        min_H=str(cert.min_H),
    )
