"""T063 concentration-compactness (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.winding_function import WindingMass, winding_grid

T063Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T063Regime = Literal["CONCENTRATED", "DIFFUSE", "MULTICENTER"]


@dataclass
class ConcentrationProfile:
    rho: float
    center: tuple[float, float]
    mass_fraction: float


@dataclass
class T063Audit:
    status: T063Status
    regime: T063Regime
    concentration: ConcentrationProfile | None
    center_count: int
    messages: list[str]


def concentration_function(
    w_grid: dict[tuple[int, int], int],
    rho: float,
    *,
    grid_n: int = 16,
    cell_area: float = 4.0 / 256,
) -> tuple[tuple[float, float], float]:
    """C_n(rho) = sup_x integral_{B(x,rho)} w^+ normalized by W^+."""
    best_x = (0.0, 0.0)
    best_mass = 0.0
    cell_r = 2.0 / max(grid_n - 1, 1)
    for i in range(grid_n):
        for j in range(grid_n):
            cx = -1.0 + 2.0 * i / max(grid_n - 1, 1)
            cy = -1.0 + 2.0 * j / max(grid_n - 1, 1)
            mass = 0.0
            for (ii, jj), v in w_grid.items():
                if v <= 0:
                    continue
                px = -1.0 + 2.0 * ii / max(grid_n - 1, 1)
                py = -1.0 + 2.0 * jj / max(grid_n - 1, 1)
                if ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5 <= rho + cell_r:
                    mass += cell_area
            if mass > best_mass:
                best_mass = mass
                best_x = (cx, cy)
    return best_x, best_mass


def classify_concentration_compactness(
    w_grid: dict[tuple[int, int], int],
    mass: WindingMass,
    *,
    c0: float = 0.25,
) -> T063Audit:
    """T063: concentrated, diffuse, or multicenter splitting."""
    rhos = [0.5, 0.3, 0.15, 0.08]
    best_frac = 0.0
    best_prof: ConcentrationProfile | None = None
    for rho in rhos:
        cx, m = concentration_function(w_grid, rho)
        frac = m / mass.positive_mass if mass.positive_mass > 0 else 0.0
        if frac > best_frac:
            best_frac = frac
            best_prof = ConcentrationProfile(rho=rho, center=cx, mass_fraction=frac)
    centers = _count_mass_centers(w_grid)
    regime: T063Regime = "DIFFUSE"
    msgs: list[str] = []
    if best_frac >= c0 and best_prof:
        regime = "CONCENTRATED"
        msgs.append(f"Concentrated: fraction={best_frac:.3f} at rho={best_prof.rho}")
    elif centers >= 2:
        regime = "MULTICENTER"
        msgs.append(f"Multicenter: {centers} separated regions")
    else:
        msgs.append("Diffuse: no small-scale concentration")
    return T063Audit(
        status="PROVED_LOCALLY_CLASSIFIER",
        regime=regime,
        concentration=best_prof,
        center_count=centers,
        messages=msgs,
    )


def _count_mass_centers(w_grid: dict[tuple[int, int], int], threshold: float = 0.5) -> int:
    pos = [(ij, v) for ij, v in w_grid.items() if v > 0]
    if not pos:
        return 0
    grid_n = 16
    xs = sorted(set(-1.0 + 2.0 * ij[0] / max(grid_n - 1, 1) for ij, _ in pos))
    if not xs:
        return 0
    clusters = 1
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > threshold:
            clusters += 1
    return clusters
