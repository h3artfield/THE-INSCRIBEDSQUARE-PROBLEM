# Child Signature Packing (Directive 047)

For node \(v\) with children \(w_i\), audit:

\[
\sum_i \Phi_{\mathrm{end}}(w_i) \stackrel{?}{\le} \theta\,\Phi_{\mathrm{end}}(v).
\]

## Geometric bound

Wedge interaction bound from center separation and hull diameter yields candidate \(\theta\). Status on singleton models: **LOOSE_CONTRACTION** — inequality holds with geometric slack but **strict** \(\theta<1\) not derived from hull inclusion alone.

**First gap:** cannot infer strict contraction merely from nested child hulls.

**Module:** `child_signature_packing.py`
