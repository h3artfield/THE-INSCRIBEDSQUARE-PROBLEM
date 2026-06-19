# Chord–Lobe Decomposition

**Status:** PROVED (general position) + limit extension (Directive 009)

---

## Setup

Simple polygonal arc \(\alpha\) from \(A=\alpha(s)\) to \(B=\alpha(t)\). Closing chord \(L=[B,A]\).

**General position:** \(L\) meets open arc transversely; finitely many interior intersections; no edge overlaps \(L\).

---

## Intersection ordering

List intersections \(q_1,\ldots,q_k\) in arc order along \(\alpha\) and in chord order along \(L\).

---

## Lobe construction

Between consecutive cut points (including \(A,B\)), each lobe \(\Gamma_j\) is:

- one subarc \(\alpha|_{I_j}\);
- one chord subsegment between its endpoints.

Interiors \(I_j\) are disjoint. Each \(\Gamma_j\) is a simple closed polygonal curve (Jordan).

---

## Winding identity

\[
[\alpha\cup L]=\sum_{j=1}^m \varepsilon_j[\Gamma_j],\qquad \varepsilon_j\in\{-1,+1\},
\]

with \(\mathcal A_\alpha(s,t)=\sum_j \varepsilon_j\mathrm{Area}(\Omega_j)\).

**Proof sketch:** planar polygonal closed walk; signed area equals sum of signed Jordan lobe areas by cutting at self-intersections on \(L\).

---

## Diameter bound

Chord subsegment \(\subseteq\) convex hull of its endpoints \(\subseteq \alpha(I_j)\) in the parameter cone, hence

\[
\mathrm{diam}(\Gamma_j)\le \mathrm{diam}(\alpha(I_j)).
\]

For any \(u,v\in I_j\), \(| \alpha(u)-\alpha(v)|\le|\alpha|_{2-var;I_j}\) (partition \(\{u,v\}\)), so \(\mathrm{diam}(\alpha(I_j))\le|\alpha|_{2-var;I_j}\).

---

## Superadditivity

For disjoint interiors covering \([s,t]\),

\[
\sum_j|\alpha|_{2-var;I_j}^2\le|\alpha|_{2-var;[s,t]}^2
\]

because a joint partition on \([s,t]\) restricting to each \(I_j\) gives \(\sum_j \omega_j^2\le\omega^2\).

---

## Implementation

`src/squarepeg/area_variation/chord_lobes.py`
