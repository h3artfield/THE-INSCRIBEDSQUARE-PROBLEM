"""Independent exact checker using SymPy (not production Gaussian elimination)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Literal

from sympy import Matrix, Rational, symbols

from squarepeg.curves.polygon import PolygonCurve

Rotation = Literal["ccw", "cw"]

FIXTURE_DIR = Path(__file__).resolve().parents[3] / "data" / "differential_fixtures"


def _sympy_rotation(kind: Rotation) -> Matrix:
    if kind == "ccw":
        return Matrix([[0, -1], [1, 0]])
    return Matrix([[0, 1], [-1, 0]])


def build_sympy_system(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> tuple[Matrix, Matrix]:
    u1, u2, u3, u4, vx, vy = symbols("u1 u2 u3 u4 vx vy")
    vars_vec = Matrix([u1, u2, u3, u4, vx, vy])
    j = _sympy_rotation(rotation)

    origins = []
    directions = []
    for idx in edges:
        o, d = polygon.edge_parametric(idx)
        origins.append(Matrix([Rational(o[0], 1), Rational(o[1], 1)]))
        directions.append(Matrix([Rational(d[0], 1), Rational(d[1], 1)]))

    eqs = []
    v = Matrix([vx, vy])
    e1 = origins[0] + u1 * directions[0]
    for i, (origin, direction, ui) in enumerate(
        zip(origins[1:], directions[1:], [u2, u3, u4]), start=1
    ):
        ei = origin + ui * direction
        if i == 1:
            target = e1 + v
        elif i == 2:
            target = e1 + v + j * v
        else:
            target = e1 + j * v
        eqs.extend((ei[0] - target[0], ei[1] - target[1]))

    A, b = Matrix(eqs).jacobian(vars_vec), Matrix(eqs).subs(
        {u1: 0, u2: 0, u3: 0, u4: 0, vx: 0, vy: 0}
    )
    # Build A,b properly by collecting linear coefficients
    rows = []
    rhs = []
    for eq in eqs:
        coeffs = [eq.coeff(var) for var in vars_vec]
        rows.append(coeffs)
        const = eq.subs({var: 0 for var in vars_vec})
        rhs.append(const)
    return Matrix(rows), Matrix(rhs)


def _build_ab_direct(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> tuple[Matrix, Matrix]:
    """Construct A,b from parametric edge data with SymPy rationals."""
    u1, u2, u3, u4, vx, vy = symbols("u1 u2 u3 u4 vx vy")
    j = _sympy_rotation(rotation)

    def edge(idx, u):
        o, d = polygon.edge_parametric(idx)
        return Matrix([Rational(o[0], 1), Rational(o[1], 1)]) + u * Matrix(
            [Rational(d[0], 1), Rational(d[1], 1)]
        )

    e1 = edge(edges[0], u1)
    v = Matrix([vx, vy])
    pairs = [
        (edge(edges[1], u2), e1 + v),
        (edge(edges[2], u3), e1 + v + j * v),
        (edge(edges[3], u4), e1 + j * v),
    ]
    eqs = []
    for lhs, rhs in pairs:
        eqs.extend([lhs[0] - rhs[0], lhs[1] - rhs[1]])

    vars_vec = [u1, u2, u3, u4, vx, vy]
    rows = []
    consts = []
    for eq in eqs:
        rows.append([Rational(eq.coeff(v), 1) for v in vars_vec])
        consts.append(Rational(eq.subs({v: 0 for v in vars_vec}), 1))
    return Matrix(rows), Matrix(consts)


@dataclass
class SympyCheckResult:
    rank: int
    nullity: int
    consistent: bool
    free_vars: int


def sympy_analyze_system(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> SympyCheckResult:
    a, b = _build_ab_direct(polygon, edges, rotation)
    aug = a.row_join(b)
    rref, pivots = aug.rref(iszerofunc=lambda x: x == 0)
    rank = len(pivots)
    n = a.cols
    consistent = True
    for r in range(rank, aug.rows):
        if rref[r, n] != 0:
            consistent = False
            break
    return SympyCheckResult(
        rank=rank,
        nullity=n - rank,
        consistent=consistent,
        free_vars=n - rank,
    )


def production_rank(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> tuple[int, bool]:
    from squarepeg.exact_squares.equations import build_square_system
    from squarepeg.exact_squares.families import solve_affine_system

    m, rhs = build_square_system(polygon, edges, rotation)
    sol = solve_affine_system(m, rhs)
    return sol.rank, sol.inconsistent


def compare_systems(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    rotation: Rotation,
) -> dict:
    prod_rank, prod_incon = production_rank(polygon, edges, rotation)
    sym = sympy_analyze_system(polygon, edges, rotation)
    return {
        "edges": edges,
        "rotation": rotation,
        "production_rank": prod_rank,
        "production_inconsistent": prod_incon,
        "sympy_rank": sym.rank,
        "sympy_nullity": sym.nullity,
        "sympy_consistent": sym.consistent,
        "match": prod_rank == sym.rank and prod_incon == (not sym.consistent),
    }


def save_fixture(data: dict, name: str) -> Path:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    path = FIXTURE_DIR / f"{name}.json"
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path
