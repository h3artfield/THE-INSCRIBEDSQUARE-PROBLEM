# Invariant Critical State Models (Directive 051)

If uniform Bellman contraction fails, extract invariant measure \(\nu\) with master slack

\[
\mathcal S_{\mathcal B}(v) = \mathcal B(X(v)) - \sum_w \mathcal B(X(w)).
\]

Zero-slack support \(\mathcal S_{\mathcal B}=0\) classifies critical models: dominant ray, finite-center, annular, thin, sign cancellation, parameter disconnection, infinite-center, or `DIFFUSE_CRITICAL_NEUTRAL_STATE_MEASURE`.

**Modules:** `invariant_state_measure.py`, `critical_state_classifier.py`
