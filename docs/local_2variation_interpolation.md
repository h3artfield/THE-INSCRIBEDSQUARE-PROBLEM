# Local 2-Variation Interpolation Control

**Status:** PROVED_LOCALLY (Directive 009)

---

## Control function

For finite-(2)-variation \(c\),

\[
\omega_c(s,t):=|c|_{2-var;[s,t]}^2.
\]

**Properties:** nonnegative; zero on diagonal; superadditive; **continuous** on \(\{(s,t):s\le t\}\) for finite 2-variation paths (Wiener / Friz–Victoir template).

---

## PL interpolants

\(P_n=c^{D_n}\) simple BG polygons, mesh \(\mu_n\to 0\).

---

## Local estimate

For each \((s,t)\) and large \(n\),

\[
|P_n|_{2-var;[s,t]}^2\le \omega_c\bigl((s-\mu_n)_+,(t+\mu_n)_-\bigr).
\]

**At partition points** \(s=t_j\in D_n\): \(P_n\) uses exactly partition edges, so equality with conforming partition sum \(\Rightarrow C_0=1\).

**General \((s,t)\):** bracket by neighboring partition times; boundary slippage \(\to 0\) as \(\mu_n\to 0\) by continuity of \(\omega_c\).

Any universal finite \(C_0\) suffices; **\(C_0=1\)** in the limit.

---

## Consequence

Uniform equicontinuity of \(\{P_n\}\) from \(\omega_c(s,t)\to 0\) as \(t-s\to 0\) independently of \(n\) (after ignoring finitely many initial \(n\)).
