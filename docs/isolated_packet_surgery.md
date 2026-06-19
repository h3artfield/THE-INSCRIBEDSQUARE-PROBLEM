# Isolated Packet Surgery

**Directive 023 Parts III–V.**

## Isolated packet disk

Parameter interval \(I=[a,b]\) with closed Jordan disk \(D\), \(\operatorname{diam}D \le r\), satisfying isolation conditions (§3).

Implementation: `packet_disk.py`.

## Replacement crosscut

Simple arc \(\sigma_I\) from \(P(a)\) to \(P(b)\) in \(\operatorname{int}D\). Straight chord when valid; collar arc otherwise.

Implementation: `crosscut.py`.

## Surgered curve

\[
S_I(P)(t) = P(t) \text{ for } t \notin I; \quad \sigma_I(t) \text{ for } t \in I.
\]

Jordan preservation verified via `PolygonCurve` simplicity check.

Implementation: `local_surgery.py`.

## T042 — Local Packet Surgery Lemma

**Status:** PROVED_LOCALLY (straight-chord case)

1. Jordan curve preserved
2. \(\|S_I(P)-P\|_\infty \le \operatorname{diam}D \le r\)
3. Relative-area defect \(O(r^2)\) (straight chord: zero on replacement arc)
4. Intervals outside \(I\) unchanged

Audit: `certify_t042()`.
