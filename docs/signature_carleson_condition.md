# SIGNATURE_CARLESON Condition

**Directive 024 Part VII.**

A packet forest sequence satisfies `SIGNATURE_CARLESON` when:

1. Maximal packet diameter \(\to 0\)
2. Maximal intervals pairwise disjoint
3. Surgeries chord-safe (`CHORD_SAFE_ISOLATED_PACKET`)
4. Retained-skeleton modulus \(\beta_n(\delta) \to 0\)
5. \(\lim_{\delta\downarrow0}\limsup_n \sup_{|J|\le\delta} |A_{\mathrm{att},n}(J)| = 0\)
6. Endpoint corrections vanish uniformly

Square mass \(\mu_2 \to 0\) **does not** imply (5).

## Strengthened sufficient versions

| Version | Implies SIGNATURE? |
|---------|-------------------|
| A — linear mass \(\mu_1 \to 0\) | Not proved |
| B — attachment (2)-variation \(\to 0\) | **Yes** (local) |
| C — fat-disk packing | Partial (mass only) |
| D — bounded multiplicity | Open |

Implementation: `signature_carleson.py`.
