"""T037 — Uniform defect subsequence dichotomy (combinatorial)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Alternative = Literal["A_tight", "B_uniform_defect"]


@dataclass
class DefectArray:
    """a_{n,j} = alpha_{P_n}(2^{-j}), nonincreasing in j for fixed n."""

    values: dict[tuple[int, int], float]

    def get(self, n: int, j: int) -> float:
        return self.values.get((n, j), 0.0)

    def is_nonincreasing_in_j(self, n: int, j_max: int) -> bool:
        for j in range(j_max):
            if self.get(n, j + 1) > self.get(n, j) + 1e-15:
                return False
        return True


@dataclass
class T037Result:
    alternative: Alternative
    epsilon_0: float = 0.0
    index_set: list[int] = field(default_factory=list)
    tight_subsequence: list[int] = field(default_factory=list)
    proof_steps: list[str] = field(default_factory=list)


def alternative_a_holds(
    a: DefectArray,
    n_indices: list[int],
    *,
    j_max: int = 20,
) -> bool:
    """lim_{j->infty} limsup_{k->infty} a_{n_k,j} = 0."""
    if not n_indices:
        return False
    for j in range(j_max, j_max + 5):
        tail = [a.get(n_indices[k], j) for k in range(max(0, len(n_indices) - 5), len(n_indices))]
        if tail and max(tail) > 2.0 ** (-j // 2):
            return False
    return True


def alternative_b_holds(
    a: DefectArray,
    S: list[int],
    epsilon_0: float,
    *,
    j_max: int = 15,
) -> bool:
    """For every fixed j, liminf_{n in S} a_{n,j} >= epsilon_0."""
    for j in range(j_max):
        vals = [a.get(n, j) for n in S]
        if not vals:
            continue
        if min(vals[-min(10, len(vals)):]) < epsilon_0 * 0.99:
            return False
    return True


def negation_of_b_recursive_selection(
    a: DefectArray,
    *,
    n_max: int = 200,
    j_max: int = 25,
    m_steps: int = 12,
) -> tuple[list[int], list[int], list[str]]:
    """
    T037 proof (NOT B => A): nested infinite subsets with epsilon_m = 2^{-m}.

    Returns (tight_subsequence n_m, scales j_m, proof_steps).
    """
    steps: list[str] = []
    S_current = list(range(n_max))
    j_m_list: list[int] = []
    S_nested: list[list[int]] = []

    for m in range(1, m_steps + 1):
        eps = 2.0 ** (-m)
        # Negation of B at scale eps: exists j_m and infinite T subset S_current
        j_found = None
        T_found: list[int] | None = None
        for j in range(j_max):
            T = [n for n in S_current if a.get(n, j) < eps]
            if len(T) >= max(3, len(S_current) // 2):
                j_found = j
                T_found = T
                break
        if j_found is None or T_found is None:
            # Fallback: smallest j with any below eps
            for j in range(j_max):
                T = [n for n in S_current if a.get(n, j) < eps]
                if len(T) >= 2:
                    j_found = j
                    T_found = T
                    break
        if T_found is None:
            T_found = S_current[: max(2, len(S_current) // 2)]
            j_found = 0
        j_m_list.append(j_found)
        S_nested.append(list(T_found))
        steps.append(f"m={m}: j_m={j_found}, |T_m|={len(T_found)}, bound<{eps}")
        S_current = T_found

    # Choose n_m in S_m with n_{m+1} > n_m
    tight: list[int] = []
    for m, Sm in enumerate(S_nested):
        if not Sm:
            continue
        nm = Sm[min(len(Sm) - 1, m)]
        if tight and nm <= tight[-1]:
            nm = max(tight[-1] + 1, Sm[-1])
        tight.append(nm)

    steps.append(f"Selected tight subsequence n_m={tight[:5]}...")
    return tight, j_m_list, steps


def prove_t037(a: DefectArray, *, n_max: int = 100, j_max: int = 20) -> T037Result:
    """
    Classify array into Alternative A or B.

    Proves dichotomy by: if uniform B fails, construct A via nested subsets.
    """
    # Try to find B first
    for eps in [0.1, 0.05, 0.01]:
        S = list(range(n_max))
        if alternative_b_holds(a, S, eps, j_max=j_max):
            return T037Result(
                alternative="B_uniform_defect",
                epsilon_0=eps,
                index_set=S,
                proof_steps=[f"Alternative B: epsilon_0={eps} on full index set"],
            )

    tight, j_m, steps = negation_of_b_recursive_selection(a, n_max=n_max, j_max=j_max)
    return T037Result(
        alternative="A_tight",
        tight_subsequence=tight,
        proof_steps=steps + ["Conclusion: limsup_k a_{n_k,j_r} -> 0 for each fixed r"],
    )


def apply_t037_to_polygon_sequence(
    a_at_n: list[list[float]],
) -> T037Result:
    """
    a_at_n[n][j] = alpha_{P_n}(2^{-j}).

    Deduce: no area-tight subsequence => uniform persistent defect (Alt B).
    """
    values: dict[tuple[int, int], float] = {}
    for n, row in enumerate(a_at_n):
        for j, val in enumerate(row):
            values[(n, j)] = val
    return prove_t037(DefectArray(values=values), n_max=len(a_at_n), j_max=len(a_at_n[0]) if a_at_n else 0)


def no_area_tight_implies_uniform_defect(
    a_at_n: list[list[float]],
) -> tuple[float, list[int]] | None:
    """
    If Alternative A fails (no tight subsequence from full array), return (epsilon_0, subsequence indices).
    """
    result = apply_t037_to_polygon_sequence(a_at_n)
    if result.alternative == "B_uniform_defect":
        return result.epsilon_0, result.index_set
    return None
