# Residual Square-Angle Vanishing (T016)

**Status:** CONJECTURAL_TARGET

---

## Residual class \(\mathcal{R}\)

Jordan curves (area normalized to \(\pi\)) that are:

- measure zero (Lebesgue image);
- not covered by AI-PEG-v3 continuous-Legendrian-lift / primitive convergence route;
- possibly nonrectifiable;
- possibly not locally monotone.

**Not claimed:** every nonrectifiable curve lies in \(\mathcal{R}\).

---

## Square-angle target (AI-PEG-v3 notation)

For \(C\in\mathcal{R}\), \(\theta=\pi/2\):

Let \(F_C\) be sheaf quantization; \(R_{\pi/2}\) square-angle action; \(a(\pi/2,C)\in(0,\pi)\) critical value (§4); \(\Delta_C\subset C\times C\) diagonal; \(\rho\) projection as in Lemma 4.2.

**Target (sign convention — verify against §4 before use):**

\[
\Gamma\left(
\rho^{-1}(\Delta_C);\,
\mu hom\left(F_C,\, T_{-a(\pi/2,C)} R_{\pi/2} F_C\right)\big|_{\rho^{-1}(\Delta_C)}
\right) \simeq 0.
\]

**Note:** AI-PEG-v3 uses \(T_{-a_\theta}\) in microsupport disjointness (Thm 4.1 proof). Translation sign must match §4, not inferred from Floer normalization.

---

## Conditional consequence

If T016 holds for every \(C\in\mathcal{R}\), then combining:

- AI-PEG-v3 positive-measure case (Remark 5.4 / Thm 1.1 proof);
- Corollaries 5.7 (rectifiable), 5.10 (locally monotone);
- T016 for \(\mathcal{R}\);

every Jordan curve inscribes a square-angle (\(\theta=\pi/2\)) rectangle, hence a square.

**Dependency:** Full universal square peg still requires connecting rectangles to squares (standard geometry) and covering all curve classes.

---

## Ledger

See **T016** in `docs/theorem_ledger.md`.
