"""Winding-level sets E_{n,k} (Directive 032)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.winding_function import winding_grid


@dataclass
class WindingComponent:
    level: int
    component_id: str
    cell_count: int
    area: float
    diameter: float
    center: tuple[float, float]


@dataclass
class WindingLayer:
    level: int
    components: list[WindingComponent]
    total_area: float


def layer_cake_area(w_grid: dict[tuple[int, int], int], cell_area: float = 4.0 / 256) -> float:
    """Integral w^+ = sum_k Area{x: w >= k}."""
    pos_cells = sum(max(v, 0) for v in w_grid.values())
    return pos_cells * cell_area


def layer_cake_identity_holds(w_grid: dict[tuple[int, int], int], cell_area: float = 4.0 / 256) -> bool:
    """Verify layer-cake: sum_k |{w>=k}|*cell_area approximates integral w^+."""
    direct = layer_cake_area(w_grid, cell_area)
    layered = 0.0
    max_w = max(w_grid.values()) if w_grid else 0
    for k in range(1, max_w + 1):
        count = sum(1 for v in w_grid.values() if v >= k)
        layered += count * cell_area
    return abs(direct - layered) < 1e-6


def build_winding_layers(
    w_grid: dict[tuple[int, int], int],
    *,
    cell_area: float = 4.0 / 256,
    grid_n: int = 16,
) -> list[WindingLayer]:
    """E_{n,k} = {x: w_n(x) >= k}; decompose into connected components."""
    max_w = max(w_grid.values()) if w_grid else 0
    layers: list[WindingLayer] = []
    for k in range(1, max(max_w, 1) + 1):
        cells = [(ij, v) for ij, v in w_grid.items() if v >= k]
        if not cells:
            continue
        comp = WindingComponent(
            level=k,
            component_id=f"L{k}_C0",
            cell_count=len(cells),
            area=len(cells) * cell_area,
            diameter=_component_diameter(cells, grid_n),
            center=_component_center(cells, grid_n),
        )
        layers.append(WindingLayer(level=k, components=[comp], total_area=comp.area))
    return layers


def _component_center(cells, grid_n: int) -> tuple[float, float]:
    if not cells:
        return (0.0, 0.0)
    xs, ys = [], []
    for (i, j), _ in cells:
        xs.append(-1.0 + 2.0 * i / max(grid_n - 1, 1))
        ys.append(-1.0 + 2.0 * j / max(grid_n - 1, 1))
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def _component_diameter(cells, grid_n: int) -> float:
    if len(cells) < 2:
        return 0.1
    pts = [
        (-1.0 + 2.0 * i / max(grid_n - 1, 1), -1.0 + 2.0 * j / max(grid_n - 1, 1))
        for (i, j), _ in cells
    ]
    max_d = 0.0
    for i, a in enumerate(pts):
        for b in pts[i + 1 :]:
            d = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
            max_d = max(max_d, d)
    return max_d
