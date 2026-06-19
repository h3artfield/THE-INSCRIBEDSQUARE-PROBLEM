# T032* — Intrinsic Degree-Collapse-to-Area-Tightness

**Status:** `CONJECTURAL_FULL_BRIDGE`

**Replaces:** certificate-based T032 (withdrawn — see F014).

---

## Statement

Let \(P_n\to\gamma\) be cyclic simple polygonal interpolants. If every subsequence with compatible protected windows satisfies

\[
\rho_\square(P_{n_k})\to 0,
\]

then there exists an area-tight subsequence.

---

## Consequence chain (if T032* proved)

1. \(\limsup\rho_\square>0\) on some subsequence \(\Rightarrow\) square (T031-B);
2. else intrinsic collapse \(\Rightarrow\) area-tight subsequence (T032*);
3. area-tight \(\Rightarrow\) every rectangle (T022).

---

## Not equivalent to old T032

Old statement used \(\underline\rho_k\to 0\) or `rho_square_certified` — **invalid** as universal bridge.

---

## Falsification routes

- **Route A:** prove persistent non-area-tightness forces fixed-scale protected box.
- **Route B:** recursive defect candidate (`recursive_defect.py`) — not verified.
