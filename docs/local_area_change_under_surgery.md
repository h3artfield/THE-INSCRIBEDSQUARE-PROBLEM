# Local Area Change Under Surgery

**Directive 023 §7–§8; corrected Directive 024.**

## Three quantities (do not conflate)

| Quantity | Symbol | Notes |
|----------|--------|-------|
| Original packet area | \(\mathcal A_P(I)\) | May be large (winding) |
| Replacement area | \(\mathcal A_{\sigma_I}(I)\) | **Zero** for straight chord |
| Area change on \(J\) | \(\mathcal A_{S_I(P)}(J)-\mathcal A_P(J)\) | **Not** \(O(r^2)\) without winding bound |

## Straight chord on \(J \subset I\)

Replacement arc has zero relative area; change on \(J\) equals removed packet contribution.

## Collar crosscut

\(|\mathcal A_{\sigma}| \le C_{\mathrm{cross}} r^2\) with \(C_{\mathrm{cross}} = \pi/4\) for the replacement arc alone.

## Accumulated surgery

For many packets, use Chen concatenation + attachment-chain area (`docs/surgery_area_concatenation.md`, `docs/attachment_chain_area.md`).

Implementation: `area_change.py`, `accumulated_surgery.py`.
