# Attachment Chain Area

**Directive 024 Part IV.**

## Maximal surgery intervals

Select maximal intervals \(I_1,\ldots,I_N\) with disjoint interiors; descendants removed with ancestor.

## Attachment points

\(a_i = P(\inf I_i)\), \(b_i = P(\sup I_i)\); after surgery, chord \([a_i,b_i]\).

## Controls on interval \(J\)

| Quantity | Definition |
|----------|------------|
| \(\mu_2(J)\) | \(\sum \operatorname{diam}(D_i)^2\) |
| \(\mu_1(J)\) | \(\sum \operatorname{diam}(D_i)\) |
| \(V_{\mathrm{att},2}(J)^2\) | Attachment-chain (2)-variation |
| \(A_{\mathrm{att}}(J)\) | Relative area of attachment polygonal chain |

**Necessary for area-tightness:** \(A_{\mathrm{att}}\) control (not implied by \(\mu_2\) alone).

Implementation: `attachment_chain.py`.
