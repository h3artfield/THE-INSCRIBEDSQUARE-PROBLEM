# Sparse Unbounded-Gate Extraction — T060 (Directive 031)

## Theorem

If \(r_n\to0\) and \(M_n r_n\to0\) (equivalently \(q_n r_n\to0\)), then \(J_{M_n}(r_n)\to0\) and fixed defect cannot remain in join terms.

## Allocation

**Signed grouping:** one sign class carries \(\ge\varepsilon_0/4\) — avoids vanishing \(1/M_n\) ear fraction.

## T060

Finite intrusion + Jordan hull + gate sparsity + T058 \(\Rightarrow\) signature-controlled surgery forest.

**Status.** PROVED_LOCALLY

**Implementation.** `sparse_gate_extraction.certify_t060`

Chain: T060 \(\Rightarrow\) T052 \(\Rightarrow\) T043R \(\Rightarrow\) T022.
