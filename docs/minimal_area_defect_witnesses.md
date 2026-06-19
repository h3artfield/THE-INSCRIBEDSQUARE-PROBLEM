# Minimal Area-Defect Witnesses

---

## Target selection

From failure of area-tight subsequence, select \(n_k\to\infty\), \(\delta_k\downarrow 0\), intervals \(I_k\) with \(|I_k|\le\delta_k\) and \(|\mathcal A_{P_{n_k}}(I_k)|\ge\varepsilon_0>0\).

---

## Gap identified (T035-GAP)

**Not proved:** that negation of area-tightness alone implies existence of such witnesses without an additional combinatorial selection lemma.

Implementation flags `selection_lemma_required=True` when extraction fails.

---

## Spatial concentration (proved)

If witnesses exist and \(P_n\to\gamma\) uniformly, then \(\operatorname{diam}P_{n_k}(I_k)\to 0\).

See `defect_witness.py`, `normalized_defect_blowups.md`.
