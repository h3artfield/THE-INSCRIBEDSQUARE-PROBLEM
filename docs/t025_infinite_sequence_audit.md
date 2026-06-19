# T025 Infinite-Sequence Audit

**Status:** Directive 011R

---

## Question

Where is the infinite sequence required for compactness?

---

## Finding 1 — Literal fixed square on all truncations

For **every** \(N\ge 3\) tested (\(N=3,\ldots,10\)), the exact solver returns rank-6 certificate with:

* identical edge indices \((0,3,5,0)\);
* identical rational parameters;
* identical rational vertices;
* identical side².

**Route B applies:** same \(N\)-independent linear system on fixed outer-arm edges. Sequence \(N_k=k+3\to\infty\) gives certified polygon squares \(Q_k=Q\) with **literal** \(Q_k=Q\) (not merely homotopic).

---

## Finding 2 — Not a compactness proof for smooth \(\Gamma\)

Vertices lie on **chords** of the PL outer arm, **not** on smooth \(\gamma_+\). Fixed off-curve points do not move onto \(\Gamma_{\mathrm{ds}}\) as \(N\to\infty\).

Compactness passage of **polygon** squares does **not** yield a square on the **smooth Jordan curve**.

---

## Finding 3 — Directive 011 misreported edges

Reported \((0,3,5,4N+1)\); actual \((0,3,5,0)\).

---

## Infinite sequence table

| Requirement | Status |
|-------------|--------|
| \(N_k\to\infty\) | yes (\(N_k=k+3\)) |
| Certified square each \(N_k\) | yes (exact rank-6) |
| Same \(Q\) for all \(N\) | yes (literal) |
| Vertices on smooth \(\Gamma\) | **no** |
| Square on infinite smooth curve | **not proved** |

---

## Verdict

**`T025_NOT_PROVED`** for inscribed square on canonical **smooth** \(\Gamma_{\mathrm{ds}}\).

Polygon sequence result: **literal fixed square for all \(N\ge 3\)** — stronger than finite sample but insufficient for smooth inscription.
