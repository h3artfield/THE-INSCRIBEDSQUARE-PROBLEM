# Double Spiral — Annular Winding (Directive 011)

**Status:** PROVED_LOCALLY (winding stability lemma)

---

## Protected annuli

For half-turn index \(j\ge 0\), define \(A_j=\{a_j<|z|<b_j\}\) from radial values of \(\gamma_+\) at quarter-turn offsets around \(\theta_j=\theta_0+j\pi/2+\pi/4\).

Protected subannulus \(A_j'\Subset A_j\) uses 35% radial width centered in \(A_j\).

Implementation: `protected_annuli.py`.

---

## Winding stability

**Lemma (uniform closeness).** Let \(\eta\) be a simple closed polygonal curve with \(\|\eta-\Gamma_{\mathrm{ds}}\|_\infty<\delta_j\), where \(\delta_j<\frac14(b_j'-a_j')\). Then the subarc of \(\eta\) crossing \(A_j'\) has winding number \(+1\) about any test point in \(A_j'\) iff the true spiral subarc does.

*Proof sketch.* In annulus \(A_j\setminus A_j'\), the two curves are within \(\delta_j\) of a graph over the angular coordinate; no vertex can enter \(A_j'\) without crossing the annulus boundary; homotopy invariance of index in \(A_j'\setminus\{\text{curve}\}\) preserves integer winding. □

---

## Area lower bound

For closed subarc-plus-chord \(\eta\):

\[
\mathcal A(\eta)=\int_{\mathbb R^2}\operatorname{wind}(\eta,z)\,dA(z).
\]

If \(\eta\) has winding \(+1\) in each \(A_j'\), \(j=1,\ldots,J\):

\[
|\mathcal A(\eta)|\ge\sum_{j=1}^J\pi\bigl((b_j')^2-(a_j')^2\bigr)/2 - E,
\]

with \(E\) bounded by chord endpoint error (Directive 011 §8).

---

## Code

`winding_stability.py`, `annular_winding.py`.
