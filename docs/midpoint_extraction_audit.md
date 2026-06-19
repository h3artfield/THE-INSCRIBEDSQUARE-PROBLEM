# Midpoint Extraction Lemma — Quantifier Audit

**Reference:** `docs/midpoint_extraction_lemma.md` (Directive 003)  
**Audit status:** `PROVED_WITH_STRENGTHENED_HYPOTHESIS`

---

## Hypothesis as written

> For all sufficiently large n, and all h ∈ (0, ε]:
> \[(g_n(½+h) - g_n(½-h))/(2h) \ge c.\]

This is **uniform in h** for late n — strong enough to transfer to g via:

\[
|g_n - g|_\infty < ch/4 \Rightarrow D_h(g) \ge c - ch/4 / h = 3c/4.
\]

Then \(\limsup_{h\downarrow0} D_h(g) \ge 3c/4 > 0\).

**Verdict:** Step 1 is valid **under this uniform hypothesis**.

---

## Dangerous diagonal (not covered by hypothesis alone)

If only: for each n, ∃h_n with slope ≥ c, or if \(\|g_n-g\|_\infty = \epsilon_n\) with \(\epsilon_n / h_n \not\to 0\), then transfer fails.

Example: \(\epsilon_n = 1/n\), \(h_n = 1/\sqrt{n}\) gives \(\epsilon_n/h_n \to \infty\).

**Uniform convergence alone** without uniform slope on shrinking windows is **insufficient**.

---

## Required strengthening (explicit)

One of:

1. **(H-uniform)** ∃N₀, ε, c>0: ∀n≥N₀, ∀h∈(0,ε], D_h(g_n)≥c; or
2. **(H-diagonal)** For each h>0, ∃n(h) with D_h(g_{n(h)})≥c and \(\|g_{n(h)}-g\|_\infty = o(h)\).

The written lemma uses (H-uniform). Label: **PROVED_WITH_STRENGTHENED_HYPOTHESIS**.

---

## Steps 2–7

Mechanism packaging from Greene–Lobb (T002, T003) is standard conditional on (H-uniform) and spectral realizability. No additional quantifier gap identified in Steps 2–7 given (H-uniform).

---

## Ledger update

T012 status → `PROVED_WITH_STRENGTHENED_HYPOTHESIS` (see `docs/theorem_ledger.md`).
