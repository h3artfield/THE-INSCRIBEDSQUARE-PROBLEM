# T029 — Protected Square Degree Theorem

**Status:** `PROVED_LOCALLY`

---

## Statement

If \((\gamma, B)\) is a **protected square box**, then \(\gamma\) contains a nondegenerate inscribed square with parameters in \(B\).

---

## Protected box definition

Four disjoint compact windows \(J_1,\ldots,J_4\subset S^1\) in cyclic boundary order; \(B=J_1\times\cdots\times J_4\).

Conditions:

1. \(0\notin F_\gamma(\partial B)\) with boundary margin \(m(\gamma,B)>0\);
2. \(\deg(F_\gamma,B,0)\ne0\);
3. positive pairwise separation margin on window images;
4. every zero in \(B\) has positive side length.

---

## Proof (Brouwer degree)

Nonzero degree \(\Rightarrow\) \(F_\gamma\) has a zero in \(B\). Square equations \(F=0\) characterize equal edge lengths and equal diagonals. Separation and side-length margins imply four distinct vertices and nondegeneracy. Cyclic boundary order is explicit in window ordering.

**No double-spiral dependence.**

Implementation: `src/squarepeg/robust_degree/protected_box.py`, `degree_certificate.py`.

---

## Consequences bundled in certificate

| Property | Source |
|----------|--------|
| Zero existence | \(\deg\ne0\) |
| Distinct vertices | separation LB |
| Positive side | side-length LB |
| Square shape | \(F=0\) equations |
| Boundary order | window cyclic order |
