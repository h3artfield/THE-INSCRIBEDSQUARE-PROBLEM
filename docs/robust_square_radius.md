# Robust Square Radius \(\rho_\square\)

**Status:** `DEFINED_AND_CERTIFIED` (Directive 014)

---

## Perturbation bound

For \(|\tilde\gamma-\gamma|_\infty\le\eta\) on the support of \(B\):

\[
|F_{\tilde\gamma}-F_\gamma|_{\infty;B} \le E_{\gamma,B}(\eta)
= 2\bigl(8D_\gamma\,\eta + 4\eta^2\bigr),
\]

where \(D_\gamma=\operatorname{diam}(\gamma)\) (translation-invariant preferred over coordinate \(R\)).

---

## Box radius

\[
\rho_\square(\gamma,B)
=
\sup\bigl\{\eta>0 : E_{\gamma,B}(\eta)<m(\gamma,B),\ \text{separation survives}\bigr\}.
\]

Curve invariant:

\[
\rho_\square(\gamma)=\sup_B \rho_\square(\gamma,B)
\]

over ordered protected boxes. **May be zero** even when squares exist.

---

## Distinctions

| Concept | Meaning |
|---------|---------|
| Square exists | Some zero of \(F\) |
| Protected box | Degree + boundary exclusion |
| \(\rho_\square>0\) | \(C^0\) robust neighborhood |

---

## Computable lower bound (polygons)

\[
\rho_\square^{\mathrm{cert}}(P)=\max_Q \rho_\square(P,B_Q)
\]

over rank-6 isolated certificates converted to protected boxes. Absence of certificate \(\ne\) mathematical zero.

Implementation: `perturbation_radius.py`, `polygon_extractor.py`.

---

## Canonical instance

Double spiral: \(\rho_\square\approx 1.1\times10^{-5}\) on certified T025 box (recovers T027).
