"""Machine-checkable square certificates."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from typing import Any, Literal, TYPE_CHECKING

from squarepeg.curves.polygon import Point, PolygonCurve

if TYPE_CHECKING:
    from squarepeg.exact_squares.solver import SquareSolution

CertificateType = Literal["exact", "interval", "family", "singular"]


def _frac_str(x: Fraction) -> str:
    return str(x)


def square_dedup_key(vertices: tuple[Point, ...]) -> tuple:
    """Canonical key modulo cyclic rotation and reversal of square vertices."""
    normalized = [
        (str(v[0]), str(v[1])) for v in vertices
    ]
    rotations = [tuple(normalized[k:] + normalized[:k]) for k in range(4)]
    reversals = [tuple(reversed(r)) for r in rotations]
    return min(rotations + reversals)


@dataclass
class SquareCertificate:
    polygon_hash: str
    edge_indices: tuple[int, int, int, int]
    edge_parameters: tuple[str, str, str, str]
    vertices: tuple[tuple[str, str], ...]
    orientation: Literal["ccw", "cw"]
    side_length_squared: str
    diagonal_length_squared: str
    residuals: dict[str, str]
    cyclic_order_verified: bool
    certificate_type: CertificateType
    side_vector: tuple[str, str] = ("0", "0")
    solve_rank: int | None = None
    family_data: dict[str, Any] = field(default_factory=dict)

    def dedup_key(self) -> tuple:
        verts = tuple((Fraction(x), Fraction(y)) for x, y in self.vertices)
        return square_dedup_key(verts)  # type: ignore[arg-type]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict) -> SquareCertificate:
        return cls(
            polygon_hash=data["polygon_hash"],
            edge_indices=tuple(data["edge_indices"]),
            edge_parameters=tuple(data["edge_parameters"]),
            vertices=tuple(tuple(v) for v in data["vertices"]),
            orientation=data["orientation"],
            side_length_squared=data["side_length_squared"],
            diagonal_length_squared=data["diagonal_length_squared"],
            residuals=data["residuals"],
            cyclic_order_verified=data["cyclic_order_verified"],
            certificate_type=data["certificate_type"],
            side_vector=tuple(data.get("side_vector", ("0", "0"))),
            solve_rank=data.get("solve_rank"),
            family_data=data.get("family_data", {}),
        )

    @classmethod
    def from_solution(cls, polygon: PolygonCurve, solution: "SquareSolution") -> SquareCertificate:
        side_sq = solution.side_vector[0] ** 2 + solution.side_vector[1] ** 2
        p1, _, p3, _ = solution.vertices
        diag_sq = (p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2
        params = solution.parameters
        from squarepeg.exact_squares.validator import build_equations_independent
        from squarepeg.exact_squares.families import residual_at

        matrix, rhs = build_equations_independent(
            polygon, solution.edge_indices, solution.rotation
        )
        x = params + solution.side_vector
        res = residual_at(matrix, rhs, x)
        residuals = {"system": str(res)}
        return cls(
            polygon_hash=polygon.polygon_hash(),
            edge_indices=solution.edge_indices,
            edge_parameters=tuple(_frac_str(p) for p in params),
            vertices=tuple(
                (_frac_str(v[0]), _frac_str(v[1])) for v in solution.vertices
            ),
            orientation=solution.rotation,
            side_length_squared=_frac_str(side_sq),
            diagonal_length_squared=_frac_str(diag_sq),
            residuals=residuals,
            cyclic_order_verified=True,
            certificate_type="exact",
            side_vector=(_frac_str(solution.side_vector[0]), _frac_str(solution.side_vector[1])),
        )

    @classmethod
    def from_family_legacy(
        cls,
        polygon: PolygonCurve,
        edges: tuple[int, int, int, int],
        rotation: Literal["ccw", "cw"],
        params: tuple[Fraction, ...],
        side: Point,
        vertices: tuple[Point, ...],
        rank: int,
        particular: tuple[Fraction, ...] | None,
        direction: tuple[Fraction, ...] | None,
    ) -> SquareCertificate:
        """Legacy wrapper; prefer AffineSquareFamily1D."""
        side_sq = side[0] ** 2 + side[1] ** 2
        p1, _, p3, _ = vertices
        diag_sq = (p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2
        family_data: dict[str, Any] = {"rank": rank}
        if particular:
            family_data["particular"] = [str(x) for x in particular]
        if direction:
            family_data["direction"] = [str(x) for x in direction]
        return cls(
            polygon_hash=polygon.polygon_hash(),
            edge_indices=edges,
            edge_parameters=tuple(_frac_str(p) for p in params),
            vertices=tuple((_frac_str(v[0]), _frac_str(v[1])) for v in vertices),
            orientation=rotation,
            side_length_squared=_frac_str(side_sq),
            diagonal_length_squared=_frac_str(diag_sq),
            residuals={"deprecated": "use AffineSquareFamily1D"},
            cyclic_order_verified=True,
            certificate_type="family",
            side_vector=(_frac_str(side[0]), _frac_str(side[1])),
            solve_rank=rank,
            family_data=family_data,
        )

    @classmethod
    def from_family(
        cls,
        polygon: PolygonCurve,
        edges: tuple[int, int, int, int],
        rotation: Literal["ccw", "cw"],
        params: tuple[Fraction, ...],
        side: Point,
        vertices: tuple[Point, ...],
        solved: object,
    ) -> SquareCertificate:
        raise DeprecationWarning("Use AffineSquareFamily1D instead of sampled family certificates")

    @classmethod
    def from_singular(
        cls,
        polygon: PolygonCurve,
        edges: tuple[int, int, int, int],
        rotation: Literal["ccw", "cw"],
        rank: int,
        matrix: list[list[Fraction]],
        rhs: list[Fraction],
    ) -> SquareCertificate:
        return cls(
            polygon_hash=polygon.polygon_hash(),
            edge_indices=edges,
            edge_parameters=("?", "?", "?", "?"),
            vertices=(("0", "0"),) * 4,
            orientation=rotation,
            side_length_squared="0",
            diagonal_length_squared="0",
            residuals={"system_rank": str(rank)},
            cyclic_order_verified=False,
            certificate_type="singular",
            solve_rank=rank,
            family_data={
                "matrix": [[str(c) for c in row] for row in matrix],
                "rhs": [str(b) for b in rhs],
            },
        )

    def verify_against_polygon(self, polygon: PolygonCurve) -> bool:
        if polygon.polygon_hash() != self.polygon_hash:
            return False
        if self.certificate_type in ("singular",):
            return True
        params = tuple(Fraction(p) for p in self.edge_parameters)
        if any(p < 0 or p > 1 for p in params):
            return False
        if Fraction(self.side_length_squared) == 0:
            return False
        for coord in self.residuals.values():
            if coord not in ("0", "(0, 0)", str((Fraction(0), Fraction(0)))):
                # residuals stored as str of tuple
                if "(0, 0)" not in coord and "(0,0)" not in coord.replace(" ", ""):
                    if coord != str((Fraction(0), Fraction(0))):
                        parsed = coord.strip("()").split(",")
                        if len(parsed) == 2:
                            if Fraction(parsed[0].strip()) != 0 or Fraction(parsed[1].strip()) != 0:
                                return False
        return True
