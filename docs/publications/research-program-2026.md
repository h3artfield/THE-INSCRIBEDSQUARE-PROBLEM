# Progress on the Inscribed Square Problem: Exact Verification, Residual Geometry, and Microlocal Reductions

**Structured findings report · October 2026**  
**Authors:** Square Peg Research Program  
**Repository:** https://github.com/h3artfield/THE-INSCRIBEDSQUARE-PROBLEM  

## Abstract

We report on a structured research program targeting the Toeplitz conjecture (every Jordan curve admits a nondegenerate inscribed square). We separate an exact computational laboratory with frozen regression gates from a microlocal analytic study of Asano–Ike normal tests on the canonical double spiral. We document local and benchmark theorems, conjectural global targets, and the remaining obstruction after uniform annular kernel removal. **We do not claim a universal proof.**

## 1. Introduction

See `website/paper.html` for the HTML edition. This markdown is the canonical repo source.

## 2. Track A — squarepeg

- Directives 001–002: exact polygon solver, T009 completeness, independent validator.
- Directives 003–057: spectral audits, intrusion trees, T103/T108 chains (fixture-local).
- Directives 058–061: residual ledger, positive-scale geometry, saturation hulls, parameter limits.
- T045R: `CONJECTURAL_FULL_EXTRACTION`.
- Verification: clean-room pytest audits; Lean formalization not yet started.

## 3. Track B — analytic archive (companion)

Key proved reductions (see companion notes summarized in `universal-proof-status.md`):

1. **Uniform annular removal:** `D_{r',η'} → D_{r,η} = 0` for `r' ≤ r/5`; replacement `M ⇝ N` in derived limits.
2. **Curved-front pushforward:** explicit formula for epigraph sources under gradient hypothesis.
3. **Cap cluster:** four branches, three levels; attaching data required for full `A_n`.
4. **Double-spiral noncollapse:** benchmark theorem with uniform side bound.

**Open:** `N_{r,η} ∘ A_n` with spiral coefficients; `RHom(-, G)`; final kernel/cokernel.

## 4. Reproducibility

```bash
pip install -e ".[dev]"
pytest -m audit tests/test_frozen_certificate_snapshot.py
pytest -m fast tests/test_directive_060.py
```

## 5. Conclusion

Substantial verified infrastructure and sharp partial results; universal conjecture remains open.
