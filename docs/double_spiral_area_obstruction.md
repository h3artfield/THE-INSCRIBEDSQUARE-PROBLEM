# Double Spiral — Area Obstruction (T024 target)

**Status:** CONJECTURAL_TARGET (Directive 010)

---

## Target T024

\(\Gamma_{\mathrm{ds}}\) admits **no** area-tight sequence of simple inscribed polygonal interpolants with cyclic vertex order.

---

## Analytic lower bound program

For truncation at \(N\) turns:

1. Natural inscribed polygon preserves winding in annuli \(A_k=\{a_k<|z|<b_k\}\).
2. Each preserved turn contributes definite signed area \(\gtrsim \log k\) (annular winding certificate).
3. Endpoint terms bounded.
4. \(\sup_{s,t}|\mathcal A_{P_N}(s,t)|\) cannot \(\to 0\) as \(N\to\infty\) with mesh \(\to 0\) if winding locked.

---

## Directive 010 verdict

**Not proved** — winding certificates implemented (`annular_winding.py`); full T024 remains open.

**Do not infer** failure of all \(C^1\) approximants from polygonal failure alone.

---

## Stronger target (separate)

No regular \(C^1\) Jordan approximants with locally uniform primitive convergence — **unresolved**.
