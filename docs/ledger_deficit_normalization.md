# Ledger Deficit Normalization (Directive 050)

For each ledger inequality \((I_k)\), \(L_k(v)\le R_k(v)\), define raw deficit \(\delta_k(v)=R_k(v)-L_k(v)\ge0\) (reversed for `MULTIGEN_PACKING`: \(\delta=P_L-(1-\eta)\Phi\)).

## Normalization

When \(\Phi(v)>0\), normalized deficit \(d_k(v)=\delta_k(v)/\Phi(v)\). Child-scale terms (`RETAINED_SKELETON`) normalize against \(m(v)\), not parent \(\Phi\).

## Total ledger deficit

\[
\Delta(v)=\sum_{k=1}^{12} c_k\,\delta_k(v)
\]

Coefficients \(c_k\) are fixed in `ledger_deficits._COEFF` from the T093 signature-budget decomposition (not tuned post hoc).

## Exception classes

| Class | Meaning |
|-------|---------|
| `ZERO_SIGNATURE_NODE` | \(\Phi(v)=0\) |
| `DEGENERATE_NORMALIZATION` | ratio undefined |
| `VANISHING_GEOMETRY_EQUALITY` | \(\delta_k=0\) by degenerate geometry |
| `UNCONTROLLED_SCALE_RATIO` | parent/child scale mismatch |

**Module:** `ledger_deficits.py`
