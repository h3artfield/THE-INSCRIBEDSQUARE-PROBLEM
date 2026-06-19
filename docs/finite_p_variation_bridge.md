# Finite p-Variation Bridge (T017)

**Status:** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED (Directive 007R)

---

## Theorem T017

Let \(c:S^1\to\mathbb R^2\) be a Jordan parametrization with finite \(p\)-variation for some \(1\le p<2\). Then \(c\) satisfies AI-PEG-v3 Theorem 1.1 and inscribes a \(\theta\)-rectangle for every \(\theta\in(0,\pi)\).

**Solved class:** Jordan curves with finite \(p\)-variation for some \(p<2\) (includes nonrectifiable examples; strictly contains rectifiable curves).

---

## Proof chain

| Step | Result | Reference |
|------|--------|-----------|
| 1 | Fix \(p<q<2\) | — |
| 2 | Simple PL \(P_n\) on \(c\), mesh \(\to 0\), Jordan | BG Thm 2.2 |
| 3 | \(P_n\to c\) uniformly | mesh \(\to 0\) |
| 4 | \(\|P_n-c\|_{q\text{-var}}\to 0\) | BG Lemma 3.1 (\(f=\mathrm{id}\)) |
| 5 | \(C^1\) Jordan \(S_n\), \(\|S_n-P_n\|_{q\text{-var}}\to 0\) | **T018** |
| 6 | \(\|S_n-c\|_{q\text{-var}}\to 0\) | triangle inequality |
| 7 | \(f_n\to f\) uniformly on compacts of \(\mathbb R\) | Young proof doc |
| 8 | Area normalize to \(\pi\) | AI-PEG-v3 Prop 5.6 |
| 9 | Apply Thm 1.1 + Remark 5.6 | AI-PEG-v3 |

---

## Variation convention

See `docs/q_variation_interpolation_proof.md` and `p_variation.py`.

---

## Directive history

| Directive | Verdict |
|-----------|---------|
| **005** | OUTCOME B — \(C^1\) smoothing not yet proved |
| **006** | OUTCOME A (internal; superseded by audit) |
| **007** | OUTCOME B — repairable \(C^1\) velocity gap |
| **007R** | OUTCOME A — cubic T018; Gate 1 passed |

---

## Nonrectifiable example

Koch snowflake boundary: finite \(p\)-var for \(p>\log 4/\log 3\); infinite length; not rectifiable. See `docs/nonrectifiable_examples.md`. Not covered by local monotonicity (AI Prop 5.9).

---

## Frontier (not addressed)

| Regime | Status |
|--------|--------|
| \(p\ge 2\) | Rough-path / area enhancement — out of scope |
| Arbitrary continuous | No canonical Young primitive |
