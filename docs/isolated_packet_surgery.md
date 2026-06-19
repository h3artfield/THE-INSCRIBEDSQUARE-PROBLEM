# T042 — CHORD_SAFE_ISOLATED_PACKET Surgery

**Status:** PROVED_LOCALLY (Directive 023, corrected Directive 024)

## Hypotheses (CHORD_SAFE_ISOLATED_PACKET)

- Isolated Jordan disk \(D\), \(\operatorname{diam}D \le r\)
- Straight endpoint chord in \(D\) avoiding retained curve
- Endpoints on \(\partial D\)

## Three quantities (do not conflate)

| Quantity | Behavior |
|----------|----------|
| \(A_P(I)\) | Original packet area — may be large (winding) |
| \(A_{\sigma_I}(I)\) | Straight chord replacement — **zero** |
| \(A_{S_I(P)}(J)-A_P(J)\) | Change on interval \(J\) — **not** \(O(r^2)\) without extra bound |

## T042 conclusion

Jordan preserved; uniform error \(\le \operatorname{diam}D\).

