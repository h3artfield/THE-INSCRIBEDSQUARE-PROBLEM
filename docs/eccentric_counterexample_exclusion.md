# Eccentric Counterexample Exclusion

**Directive 021 Part III.**

## Directive 020 falsification family

Thin nested ellipses with semiaxes \(a_j \gg b_j\) have

\[
K_j = \frac{\max_\theta r_j(\theta)}{\min_\theta r_j(\theta)} = \frac{a_j}{b_j} \to \infty.
\]

Hence every fixed-\(K\) annular-graph class excludes this family for any finite \(K\).

Audit: `eccentricity_audit.directive_020_falsification_excluded()`.

## Not a relabeling

The failed Directive 020 comparison used nesting, scale control, separation, and area fullness without eccentricity control. `ANNULAR_GRAPH` adds explicit radial-graph regularity; thin ellipses fail the \(K\)-bound while satisfying earlier heuristics.

## Counterexample search (Part 6)

Attempted falsifications (`search_annular_counterexamples()`):

| Attempt | Result |
|---------|--------|
| Thin eccentric ellipse | Excluded by \(K\) |
| Off-center circles | Excluded by center drift |
| Angular ripple | Excluded by angular \(L\) |
| Rapid center drift | Excluded by \(\zeta\) |

No packet was found that satisfies `ANNULAR_GRAPH` and defeats reference closeness in the certified regime.
