"""Local packet surgery S_I(P) (Directive 023)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.defect_surgery.crosscut import Crosscut, chord_intersects_retained, straight_chord_crosscut
from squarepeg.defect_surgery.packet_disk import PacketDisk, Point, validate_isolated_packet


@dataclass
class SurgeryResult:
    original_vertices: list[Point]
    surgered_vertices: list[Point]
    is_jordan: bool
    uniform_error: float
    crosscut: Crosscut
    messages: list[str]


def apply_local_surgery(
    vertices: list[Point],
    disk: PacketDisk,
    crosscut: Crosscut | None = None,
) -> SurgeryResult:
    """Replace interval [i0,i1] with crosscut; verify Jordan property (i0 <= i1, no wrap)."""
    i0, i1 = disk.interval_start, disk.interval_end
    if i0 > i1:
        return SurgeryResult(
            original_vertices=vertices,
            surgered_vertices=vertices,
            is_jordan=False,
            uniform_error=0.0,
            crosscut=straight_chord_crosscut(vertices[i0], vertices[i1]),
            messages=["Wrap-around intervals require cyclic surgery (not implemented)"],
        )

    audit = validate_isolated_packet(vertices, disk, max_diameter=disk.diameter)
    p_a = vertices[i0]
    p_b = vertices[i1]
    cross = crosscut or straight_chord_crosscut(p_a, p_b)

    new_verts = vertices[:i0] + [p_a] + cross.interior_points + [p_b] + vertices[i1 + 1 :]
    retained = vertices[:i0] + vertices[i1 + 1 :]

    is_jordan = False
    msgs: list[str] = []
    try:
        if len(new_verts) >= 3:
            PolygonCurve([(float(x), float(y)) for x, y in new_verts])
            is_jordan = True
            msgs.append("PolygonCurve simplicity verified")
    except ValueError as e:
        msgs.append(str(e))

    if chord_intersects_retained(cross, retained):
        is_jordan = False
        msgs.append("Crosscut intersects retained curve")

    if not audit.is_isolated:
        msgs.append("Packet disk isolation audit failed")

    return SurgeryResult(
        original_vertices=vertices,
        surgered_vertices=new_verts,
        is_jordan=is_jordan,
        uniform_error=disk.diameter,
        crosscut=cross,
        messages=msgs,
    )
