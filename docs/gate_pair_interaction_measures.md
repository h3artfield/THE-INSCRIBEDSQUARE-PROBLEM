# Gate Pair Interaction Measures — Ω_v (Directive 055)

## Definition

\(\Omega_v\) is a measure on \(\mathcal M_{\mathrm{gate}} \times \mathcal M_{\mathrm{gate}}\) encoding ordered pairs \(i \ne j\) with interaction weight for

\[
\frac12\sum_{i<j}\Delta_i \wedge \Delta_j.
\]

Each pair atom carries \(\epsilon_{ij} \in \{-1,0,+1\}\) for traversal orientation.

## Exact reconstruction

On finite transitions,

\[
A_{\mathrm{cross}}(v) = \frac12 \int \epsilon(m,m')\,\Delta(m)\wedge\Delta(m')\,d\Omega_v(m,m').
\]

Also recovers inversion energy, monotone-block data, boundary/parameter interleaving, and cross-component interaction.

## Consistency

Marginal consistency with \(\Pi_v\) is enforced; pair measure is ordered (not symmetric); diagonal pairs excluded.

**Module:** `gate_pair_interaction_measure.py`
