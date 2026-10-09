# Square Peg Research Program

Computational laboratory for the **Toeplitz inscribed square conjecture**:

> Every continuous Jordan curve in the plane contains four distinct points forming a nondegenerate square.

This repository provides **exact finite geometry tools**—certified polygon square solvers, curve models, and a theorem ledger. It does **not** claim to prove or disprove the full conjecture.

## Public website

After GitHub Pages is enabled (Settings → Pages → Source: **GitHub Actions**), the site deploys from `website/` on each push to `main`:

**https://h3artfield.github.io/THE-INSCRIBEDSQUARE-PROBLEM/**

Overview, research paper, and test/evidence documentation live there. Markdown source: `docs/publications/research-program-2026.md`.

## Status

- **Directives 001–060:** frozen (latest tag `directive-060-non-jordan-saturation-hull-internal-2026-06-22`)
- **Directive 061:** parameter-disconnected limit geometry — code + docs in repo; **manifest freeze pending** full milestone regression
- **Regression:** tier 1 (`fast`) + tier 2 (`audit`) for daily work; tier 4 (`fast or deep`) before tags (~314 tests, overnight)
- **Universal conjecture:** not proved — see `docs/publications/universal-theorem-gap-plain-language.md`
- **Lean formalization:** not started (`formal/SquarePeg/` placeholder)

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
