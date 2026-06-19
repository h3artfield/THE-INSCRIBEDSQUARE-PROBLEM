# Square Peg Research Program

Computational laboratory for the **Toeplitz inscribed square conjecture**:

> Every continuous Jordan curve in the plane contains four distinct points forming a nondegenerate square.

This repository provides **exact finite geometry tools**—certified polygon square solvers, curve models, and a theorem ledger. It does **not** claim to prove or disprove the full conjecture.

## Status

- **Directive 001:** exact polygon foundation (PolygonCurve, square solver, certificates)
- Adversarial optimization, Floer computation, and full-conjecture claims are **out of scope** until later milestones

## Install

```bash
pip install -e ".[dev]"
```

## Run tests

```bash
pytest tests/ -m fast -v    # CI default (~2 min)
pytest tests/ -m slow -v    # includes oracle cross-check
python -m squarepeg.benchmarks.run
```

## Layout

| Path | Purpose |
|------|---------|
| `docs/theorem_ledger.md` | Tracked claims with proof status |
| `src/squarepeg/` | Core library |
| `tests/` | Unit and integration tests |
| `artifacts/` | Directive reports and experiment outputs |
| `formal/SquarePeg/` | Lean formalization (future) |

## Protocol

- Exact rational arithmetic is the certificate source; floating-point solvers are test oracles only.
- No numerical result is described as a proof of the universal conjecture.
