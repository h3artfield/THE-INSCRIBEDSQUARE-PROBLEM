# T021 — Simple-Arc Area–Variation Inequality

**Status:** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED (Directive 009)

---

## Statement

For every simple polygonal arc \(\alpha:[s,t]\to\mathbb R^2\),

\[
\bigl|\mathcal A_\alpha(s,t)\bigr|
\le \frac{\pi}{4}\,|\alpha|_{2-var;[s,t]}^2.
\]

---

## Relative area

\[
\mathcal A_\alpha(s,t)
=\frac12\int_s^t\Bigl[(x(u)-x(s))\,d\xi(u)-(\xi(u)-\xi(s))\,dx(u)\Bigr].
\]

Equivalent to signed area of \(\alpha\cup L\) where \(L=[\alpha(t),\alpha(s)]\) (chord closure).

---

## Proof (general position)

1. Decompose \(\alpha\cup L\) into Jordan lobes \(\Gamma_j\) with disjoint parameter subarcs \(I_j\).
2. \(\mathcal A_\alpha=\sum_j \varepsilon_j\mathrm{Area}(\Omega_j)\).
3. Isodiametric: \(\mathrm{Area}(\Omega_j)\le\frac\pi4\mathrm{diam}(\Gamma_j)^2\).
4. \(\mathrm{diam}(\Gamma_j)\le\mathrm{diam}(\alpha(I_j))\le|\alpha|_{2-var;I_j}\).
5. Superadditivity: \(\sum_j|\alpha|_{2-var;I_j}^2\le|\alpha|_{2-var;[s,t]}^2\).

See `docs/chord_lobe_decomposition.md`.

---

## Degenerate cases (§9)

Handled by:

- **Zero-area** collinear overlaps: inequality trivial.
- **Vertex on chord / tangency:** subdivide at degeneracy points (finite list).
- **Edge on chord:** split into collinear + transversal subarcs.
- **Limit:** perturb chord by \(\varepsilon\) normal translation; pass \(\varepsilon\to 0\) using upper semicontinuity of \(|\mathcal A|\) and continuity of 2-variation on polygonal arcs.

---

## Constant verdict

```text
C = π/4 PROVED
```

Adversarial search (`adversarial_arcs.py`): max ratio \(\approx\pi/8\) on semicircle; no counterexample found.

---

## Type

**LOCALLY PROVED LEMMA** — load-bearing for T019.
