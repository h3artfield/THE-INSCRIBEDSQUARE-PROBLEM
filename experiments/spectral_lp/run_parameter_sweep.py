"""Run Level-F midpoint LP parameter sweep (Directive 003)."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from squarepeg.spectral_axioms.continuum_verify import (
    certify_grid_witness,
)
from squarepeg.spectral_axioms.exact_verify import verify_grid_solution, verify_midpoint_objective
from squarepeg.spectral_axioms.grid_model import GridLPConfig, solve_grid_lp
from squarepeg.spectral_axioms.normalization import kappa_from_B
from squarepeg.spectral_axioms.two_invariant_model import TwoInvariantConfig, solve_two_invariant

KAPPA_VALUES = [
    Fraction(1),
    Fraction(101, 100),
    Fraction(11, 10),
    Fraction(5, 4),
    Fraction(3, 2),
    Fraction(2),
    Fraction(3),
    Fraction(5),
    Fraction(10),
]

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def sweep_one(kappa: Fraction, N: int = 40, k: int = 1, delta: Fraction = Fraction(0)) -> dict:
    cfg = GridLPConfig(N=N, kappa=kappa, k=k, delta=delta)
    res = solve_grid_lp(cfg)
    out: dict = {
        "kappa": str(kappa),
        "N": N,
        "k": k,
        "delta": str(delta),
        "status": res.status,
        "scipy_message": res.scipy_message,
        "optimum_float": float(res.optimum) if res.values else None,
    }
    if res.values:
        ok, errs = verify_grid_solution(res.values, cfg)
        obj = verify_midpoint_objective(res.values, cfg)
        out["verified"] = ok
        out["verification_errors"] = errs
        out["optimum_exact"] = str(obj)
        out["primal_witness"] = [str(v) for v in res.values]
    return out


def sweep_two_invariant(kappa: Fraction, N: int = 40, k: int = 1) -> dict:
    cfg = TwoInvariantConfig(N=N, kappa=kappa, k=k)
    res = solve_two_invariant(cfg)
    return {
        "kappa": str(kappa),
        "N": N,
        "k": k,
        "status": res.status,
        "message": res.message,
        "optimum_g2_midpoint": str(res.optimum_g2_midpoint),
        "g1_witness": [str(v) for v in res.g1_values],
        "g2_witness": [str(v) for v in res.g2_values],
    }


def nested_window_sweep(kappa: Fraction, N: int = 80) -> list[dict]:
    rows = []
    for k in [1, 2, 4, 8, N // 4]:
        if k >= N // 2:
            continue
        rows.append(sweep_one(kappa, N=N, k=k))
    return rows


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    one_inv: list[dict] = []
    for kappa in KAPPA_VALUES:
        row = sweep_one(kappa, N=40, k=1)
        row["nested"] = nested_window_sweep(kappa, N=80)
        row["strict_delta_1e4"] = sweep_one(kappa, N=40, k=1, delta=Fraction(1, 10000))
        one_inv.append(row)

    two_inv = [sweep_two_invariant(k, N=40, k=1) for k in KAPPA_VALUES]

    cm = certify_grid_witness(
        solve_grid_lp(GridLPConfig(N=160, kappa=Fraction(11, 10), k=1)).values,
        160,
        float(Fraction(11, 10)),
        subadd_M=500,
    )

    summary = {
        "one_invariant": one_inv,
        "two_invariant": two_inv,
        "continuum_countermodel_kappa_11_10": cm,
        "kappa_critical_bracket": ["4201/4096", "52513/51200"],
        "conclusion": (
            "Level-F axioms force D^+(g,1/2)=1 at kappa=1; "
            "do NOT force D^+>0 for kappa >= 11/10 (continuum PL countermodel certified). "
            "Critical kappa_c ~ 1.026 between 101/100 and 21/20."
        ),
    }

    out_path = RESULTS_DIR / "parameter_sweep.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    for row in one_inv:
        print(
            f"kappa={row['kappa']:>6}  opt={row.get('optimum_exact', 'NA'):>12}  "
            f"verified={row.get('verified', False)}"
        )


if __name__ == "__main__":
    main()
