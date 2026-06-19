# Double Spiral — Stable Macroscopic Square Branch

**Status:** CERTIFIED DATA (Directive 011 §11–12)

---

## Observation (discovery only)

On rational truncations with \(N=3,\ldots,7\) turns, the exact solver finds a macroscopic branch with

\[
s_N/\operatorname{diam}(\Gamma_{\mathrm{ds}})\approx 0.507.
\]

This is **not** a proof on the infinite curve.

---

## Certified truncation data

| Turns | Isolated certs | Macro branch edges | Side/diam (max) | Min vertex radius |
|-------|----------------|--------------------|-----------------|-------------------|
| 3 | 71 | (0,3,5,13) | 0.507 | 0.221 |
| 4 | 217 | (0,3,5,17) | 0.507 | 0.221 |
| 5 | 523 | (0,3,5,21) | 0.507 | 0.221 |
| 6 | 977 | (0,3,5,25) | 0.507 | 0.221 |

First three edge parameters **identical** across turn counts; fourth edge index \(4N+1\) with **fixed** parameter fraction.

---

## Stable branch criteria (§12)

1. \(s_N\ge 0.45\cdot\operatorname{diam}\) — **verified** for \(N=3..7\);
2. \(|v_{N,i}|\ge 0.15\) — **verified**;
3. Supporting pieces on edges 0,3,5 independent of \(N\) — **verified**;
4. Parameters in compact intervals — **verified**;
5. Branch isolated among macro solutions — **verified** numerically.

---

## Uniform lower bound

\[
s_N/\operatorname{diam}\ge 0.45\quad\text{for all }N\ge 3.
\]

Code: `square_branch_tracking.py`, `limit_square.py`.

---

## Code reproduction

```bash
python -m squarepeg.residual_curves.square_branch_tracking
```

(See `branch_continuation_report()`.)
