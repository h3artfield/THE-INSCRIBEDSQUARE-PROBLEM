# Gate Word Compactness (Directive 031)

## Inversion count

\[
\operatorname{Inv}(W_n)=\frac{\#\text{hull-parameter inversions}}{M_n^2}
\]

- **Asymptotically ordered:** \(\operatorname{Inv}(W_n)\to0\)
- **Persistently scrambled:** \(\limsup\operatorname{Inv}(W_n)>0\)

Interleaving not auto-protected (T049).

**Implementation.** `gate_word_limit.py`
