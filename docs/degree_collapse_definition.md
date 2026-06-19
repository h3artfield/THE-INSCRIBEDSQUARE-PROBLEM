# Degree Collapse — Definition

**Status:** `FORMALIZED` (Directive 014)

---

## Definition

For polygonal approximants \(P_n\to\gamma\), **robust square degree collapses** when

\[
\rho_\square^{\mathrm{cert}}(P_n)\to 0.
\]

---

## Mechanisms (non-exhaustive)

| Mode | Description |
|------|-------------|
| Side \(\to0\) | Squares shrink |
| Parameter collision | Two vertices merge in parameter space |
| Jacobian singular | \(\det DF\to0\) |
| Family merge | Isolated branch becomes rank-5 family |
| Boundary cross | Zero exits protected box |
| Window drift | Support migrates into wild tail |

---

## Not equivalent to absence of squares

Degree collapse \(\not\Rightarrow\) no inscribed square. A curve may have \(\rho_\square=0\) while squares exist without protected certification.

---

## Certificate vs mathematics

\(\rho_\square^{\mathrm{cert}}=0\) may mean:

- no protected square;
- solver found none;
- all squares are families;
- interval overestimation;
- unsupported rank-\(\le4\) systems.

Every experiment records interpretation via `SearchInterpretation` enum.

Implementation: `collapse_classifier.py`.
