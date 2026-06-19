"""Clean vs dirty lobe classification (Directive 027)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.area_variation.chord_lobes import Lobe, shoelace_abs
from squarepeg.defect_surgery.crosscut import straight_chord_crosscut, chord_intersects_retained
from squarepeg.defect_surgery.packet_disk import PacketDisk, disk_from_interval

Point = tuple[float, float]


@dataclass
class CleanLobeAudit:
    is_clean: bool
    chord_safe: bool
    enclosed_area: float
    diameter: float
    eligible_for_t042: bool


def lobe_to_disk(lobe: Lobe, i0: int, i1: int) -> PacketDisk:
    verts = lobe.closed_vertices()
    return disk_from_interval(verts, 0, len(verts) - 1, padding=0.02)


def audit_clean_lobe(
    lobe: Lobe,
    retained_vertices: list[Point],
    i0: int,
    i1: int,
) -> CleanLobeAudit:
    """
    Clean: P(S^1 \\ I_L) cap int(Omega_L) = empty.
    Chord-safe: straight chord avoids retained curve.
    """
    disk = lobe_to_disk(lobe, i0, i1)
    interior_pts = list(lobe.arc_vertices[1:-1]) if len(lobe.arc_vertices) > 2 else []
    is_clean = True
    for rv in retained_vertices:
        from squarepeg.defect_surgery.packet_disk import point_in_disk_interior

        if point_in_disk_interior(rv, disk):
            is_clean = False
            break

    cross = straight_chord_crosscut(lobe.chord[0], lobe.chord[1])
    chord_safe = not chord_intersects_retained(cross, retained_vertices)
    area = shoelace_abs(lobe.closed_vertices())
    diam = disk.diameter
    return CleanLobeAudit(
        is_clean=is_clean,
        chord_safe=chord_safe,
        enclosed_area=area,
        diameter=diam,
        eligible_for_t042=is_clean and chord_safe,
    )
