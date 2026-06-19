# Directive 021 Report — Annular-Graph Defect Packets

**Date:** 2026-06-18  
**Verdict:** **Outcome A — T036-N1-ANN proved** (packet-scale square theorem in certified annular-graph class)

---

## Part I — Repository stability

| Item | Status |
|------|--------|
| Directive 020 fixes (import, cwd, slow marker) | Present in tree at `5bd1377` |
| Tag `directive-020-annular-hypothesis-internal-2026-06-18` | Applied at verified commit |
| `artifacts/directive_020_verified_internal_manifest.json` | Updated with suite results |
| Fast suite ×2 | Recorded in manifest |
| Slow deterministic suite | Recorded separately |

---

## Part II–IV — ANNULAR_GRAPH and reference

- Quantitative definition: `docs/annular_graph_definition.md`
- Reference certificate: `artifacts/reference_annular_cyclic_certificate.json`
- Frozen model: star-annular \(\Gamma_{\mathrm{ref}}\), \(\rho_{\mathrm{cyc}} \approx 0.0137\), T039 rank DG\(=3\), \(w_1=1\)

---

## Part V — Comparison bound

\[
\Psi \le C_1(K-1) + C_2 L \ell_{\mathrm{win}} + C_3(g_+-g_-) + C_4 w_{\mathrm{corr}} + C_5 \zeta + C_6|g_*-g_{\mathrm{ref}}|
\]

Certified regime: \(K=1.005\), \(L=0.01\), \(\Psi \approx 0.0118 < \rho_{\mathrm{cyc}}\).

Example packet: `example_certified_packet()` (nearly circular ellipses, \(a/b=1.005\)).

---

## Part VI — T036-N1-ANN

**Status:** `PROVED_LOCALLY`

- Two controlled layers suffice (\(m_0=2\))
- Side bound: \(\operatorname{side}(Q) \ge c_{\mathrm{ann}} d_{L_j}\), \(c_{\mathrm{ann}}=0.12\)

Proof: `docs/t036_n1_annular_proof.md`; audit `certify_t036_n1_ann()`.

---

## Part VII — Limit consequences

| Claim | Status |
|-------|--------|
| Packet-scale square | PROVED |
| Positive-scale limit corollary (\(\limsup r_n>0\)) | PROVED_LOCALLY |
| Shrinking packets (\(r_n\to0\)) | Does **not** close T032§ |
| T036-N2, T036-N3 | CONJECTURAL |

---

## Part VIII — Cross-scale

Diagnostic only; no certified cross-scale rhombus. T036-N3 open.

---

## Part IX — Illustrations

- `illustrations/nested_lobe_bridge.svg/pdf/png`
- `illustrations/nested_lobe_animation_storyboard.md`
- `illustrations/nested_lobe_bridge_preview.mp4` (explanatory prototype)

---

## Part X — Reviewer questions

| # | Question | Answer |
|---|----------|--------|
| 1 | ANNULAR_GRAPH excludes Directive 020 eccentric examples? | **Yes** — \(K=a/b\to\infty\) |
| 2 | Radial-graph representation guaranteed? | **Yes** under explicit hypotheses (not from nesting alone) |
| 3 | Four windows genuine cyclic subarcs? | **Yes** in certified correspondence |
| 4 | Orientation preserving? | **Yes** |
| 5 | \(\Psi\) derived not assumed? | **Yes** — explicit coefficients in `packet_reference_bound.py` |
| 6 | Certified regime nonempty? | **Yes** — \(K=1.005\) example |
| 7 | T039 margins intact? | **Yes** — \(\Psi < \rho_{\mathrm{cyc}}\) |
| 8 | Square packet-scale or fixed-scale? | **Packet-scale**; fixed only if \(\limsup r_n>0\) |
| 9 | Positive-scale compactness valid? | **Yes** — T002 extraction |
| 10 | Illustrations labeled consistently? | **Yes** — proved / conditional / open |

---

## Part XI — Verdict

**Outcome A:** The annular-graph nested class has a complete packet-scale square theorem (T036-N1-ANN).

Positive-scale limit corollary is also proved under \(\limsup r_n>0\); not upgraded to Outcome B as primary verdict because macroscopic T032§ remains open.

---

## Code and tests

Modules: `annular_graph.py`, `eccentricity_audit.py`, `radial_correspondence.py`, `packet_reference_bound.py`, `annular_graph_certificate.py`, `positive_scale_compactness.py`, `recursive_annular_model.py`

Tests: `tests/test_annular_graph.py` (18 tests)
