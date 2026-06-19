# Area Anomaly Constructions (Exploratory)

**Status:** NUMERICAL / HEURISTIC ONLY — not proofs of T019 failure or success  
**Gate 1:** Not passed — constructions are research sketches

---

## Goal

Find polygonal Jordan sequences \(P_n\to c\) with:

- \(c\) finite 2-variation;
- \(\|P_n-c\|_{2\text{-var}}\to 0\);
- primitive functions \(f_n\) **fail** to converge or have **two** limit points.

Only **P2-D** (T019 disproved) requires a **nonexistence** result for **every** good approximating sequence.

---

## Candidate families (not verified)

### 1. Alternating fjords

Thin inward/outward zigzags on opposite sides of a base arc. Enclosed area converges; local Lévy area may oscillate.

### 2. Nested combs

Comb teeth with heights \(\sim 1/n\), widths \(\sim 1/n^2\). Total 2-variation bounded; area packets alternate sign.

### 3. Opposing spiral corridors

Logarithmic spiral channels with alternating orientation — may force winding ambiguity on closure.

### 4. Thin zigzag ribbons

Parallel zigzags with amplitude \(a_n\to 0\), frequency \(n\). \(\|P_n-c\|_{2\text{-var}}\) controlled; \(\int \xi\,dx\) sensitive to phase.

---

## Distinctions (required)

| Phenomenon | Implication |
|------------|-------------|
| One bad approximation method | Method failure only |
| Every sequence fails | Would refute T019 |
| Two subsequential primitive limits | Nonuniqueness of enhancement |

---

## Repository status

No rigorously verified counterexample constructed. Exploratory code not added (would risk misinterpretation as proof).

---

## Next step (after Gate 1)

Implement controlled 2-variation polygonal builders and track \(\mathbb A_n(s,t)\) on dyadic windows.
