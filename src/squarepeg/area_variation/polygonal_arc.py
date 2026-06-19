"""Polygonal arc utilities for T021 / T019 program."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

Point = tuple[float, float]


@dataclass(frozen=True)
class PolygonalArc:
    """Simple polygonal arc alpha: vertices in parameter order (s -> t)."""

    vertices: tuple[Point, ...]

    def __post_init__(self) -> None:
        if len(self.vertices) < 2:
            raise ValueError("arc requires at least two vertices")

    @property
    def start(self) -> Point:
        return self.vertices[0]

    @property
    def end(self) -> Point:
        return self.vertices[-1]

    @property
    def n_edges(self) -> int:
        return len(self.vertices) - 1

    def edge(self, i: int) -> tuple[Point, Point]:
        return self.vertices[i], self.vertices[i + 1]

    def subarc(self, i: int, j: int) -> PolygonalArc:
        """Inclusive vertex indices i..j."""
        if not (0 <= i < j < len(self.vertices)):
            raise ValueError("invalid subarc range")
        return PolygonalArc(self.vertices[i : j + 1])

    @classmethod
    def from_points(cls, points: Sequence[Point]) -> PolygonalArc:
        return cls(tuple(points))
