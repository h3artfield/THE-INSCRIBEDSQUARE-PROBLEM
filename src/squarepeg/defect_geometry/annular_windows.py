"""Four cyclic window extraction from nested lobe layers."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_geometry.nested_chain import NestedChain, NestedClassParams, find_same_sign_chain
from squarepeg.defect_geometry.lobe_tree import LobeTree

Window = tuple[float, float]


@dataclass
class AnnularWindows:
    """J1..J4: outer-in, inner-in, inner-out, outer-out parameter intervals."""

    j1: Window
    j2: Window
    j3: Window
    j4: Window
    layer_outer_index: int
    layer_inner_index: int
    q_separation: int


def extract_windows(
    tree: LobeTree,
    *,
    j: int = 0,
    k: int | None = None,
    q0: int = 1,
) -> AnnularWindows | None:
    """
    From boundaries of L_j and L_k, assign four disjoint cyclic-ordered intervals.

    Uses parameter subintervals on the root arc proportional to lobe nesting depth.
    """
    chain = find_same_sign_chain(tree)
    if chain.depth < 2:
        return None
    k_idx = k if k is not None else min(j + q0, chain.depth - 1)
    if k_idx >= chain.depth or j >= k_idx:
        return None
    outer = chain.lobes[j]
    inner = chain.lobes[k_idx]
    lo_o, hi_o = outer.interval
    lo_i, hi_i = inner.interval
    span = hi_o - lo_o
    if span <= 0:
        return None
    # Cyclic quadrants within outer lobe parameter range
    q = span / 4
    j1 = (lo_o, lo_o + q)
    j2 = (lo_o + q, lo_o + 2 * q)
    j3 = (lo_o + 2 * q, lo_o + 3 * q)
    j4 = (lo_o + 3 * q, hi_o)
    return AnnularWindows(
        j1=j1,
        j2=j2,
        j3=j3,
        j4=j4,
        layer_outer_index=j,
        layer_inner_index=k_idx,
        q_separation=k_idx - j,
    )


def windows_disjoint(w: AnnularWindows, tol: float = 1e-9) -> bool:
    intervals = [w.j1, w.j2, w.j3, w.j4]
    for i in range(4):
        for j in range(i + 1, 4):
            a0, a1 = intervals[i]
            b0, b1 = intervals[j]
            if not (a1 <= b0 + tol or b1 <= a0 + tol):
                return False
    return True
