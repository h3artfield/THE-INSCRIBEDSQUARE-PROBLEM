# T017 — Frozen Statement (Directive 007)

**Freeze date:** 2026-06-18  
**Status:** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED (Directive 007R)

---

## Frozen theorem (T017)

Let \(c:S^1\to\mathbb R^2\) be a Jordan parametrization of finite \(p\)-variation for some \(1\le p<2\). Then \(c\) satisfies the hypotheses of Asano–Ike Theorem 1.1 and therefore inscribes a \(\theta\)-rectangle for every \(\theta\in(0,\pi)\).

---

## Frozen supporting lemma (T018)

Let \(P:S^1\to\mathbb R^2\) be a simple polygonal Jordan curve. For every \(\varepsilon>0\) and \(q\ge 1\), there exists a regular \(C^1\) Jordan curve \(S\) with the same orientation and a common orientation-preserving parametrization such that \(\|S-P\|_\infty<\varepsilon\) and \(\|S-P\|_{q\text{-var}}<\varepsilon\).

---

## Scope limits (not strengthened)

- Does **not** claim arbitrary continuous Jordan curves.
- Does **not** claim finite \(p\)-variation for \(p\ge 2\).
- Does **not** claim external publication, peer review, or author confirmation.
- Does **not** claim Koch snowflake is outside local monotonicity (only outside rectifiability).

---

## Dependencies (frozen)

| Component | Source |
|-----------|--------|
| Polygonal Jordan approximants, \(\|P_n-c\|_{q\text{-var}}\to 0\) | BG-INTERPOLATION-v2 Thm 2.2, Lemma 3.1 |
| \(C^1\) smoothing | T018 (repository) |
| Young primitive convergence | Repository proof |
| Rectangular peg conclusion | AI-PEG-v3 Thm 1.1 |

---

## Audit gate

Clean-room audit must pass before status upgrade or Part VIII (\(p=2\)) work.
