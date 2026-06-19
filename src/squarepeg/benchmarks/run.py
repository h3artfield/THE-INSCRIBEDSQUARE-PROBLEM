"""Benchmark harness for exact square solver."""

from __future__ import annotations

import json
import subprocess
import sys
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path

from squarepeg import __version__
from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.exact_squares.validator import (
    validate_affine_family_1d,
    validate_square_certificate,
)

DEFAULT_CORPUS = Path(__file__).resolve().parents[3] / "data" / "benchmark_polygons.json"


@dataclass
class BenchmarkRecord:
    polygon_hash: str
    num_vertices: int
    quadruples_examined: int
    quadruples_pruned: int
    isolated_count: int
    families_1d_count: int
    unsupported_count: int
    rank_histogram: dict[str, int]
    validation_failures: int
    runtime_seconds: float
    peak_memory_kb: float


def _git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        )
        return out.strip()
    except Exception:
        return "unknown"


def run_benchmark(corpus_path: Path | None = None) -> dict:
    path = corpus_path or DEFAULT_CORPUS
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        polygons = [PolygonCurve(entry["vertices"]) for entry in data["polygons"]]
    else:
        polygons = [
            PolygonCurve([(0, 0), (4, 0), (4, 4), (0, 4)]),
            PolygonCurve([(0, 4), (3, 3), (2, 1), (10, 8)]),
            PolygonCurve([(0, 0), (6, 0), (6, 3), (0, 3)]),
        ]

    tracemalloc.start()
    records: list[BenchmarkRecord] = []
    rank_hist: dict[str, int] = {"6": 0, "5": 0, "le4": 0}

    for poly in polygons:
        t0 = time.perf_counter()
        result = solve_polygon_full(poly)
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()

        val_fail = 0
        for cert in result.isolated:
            from squarepeg.exact_squares.validator import validate_square_certificate

            if not validate_square_certificate(poly, cert).ok:
                val_fail += 1
        for fam in result.families_1d:
            if not validate_affine_family_1d(poly, fam).ok:
                val_fail += 1

        rank_hist["6"] += result.stats.get("isolated_count", 0)
        rank_hist["5"] += len(result.families_1d)
        rank_hist["le4"] += len(result.unsupported)

        records.append(
            BenchmarkRecord(
                polygon_hash=poly.polygon_hash(),
                num_vertices=poly.num_edges,
                quadruples_examined=result.stats.get("quadruples_examined", 0),
                quadruples_pruned=result.stats.get("quadruples_pruned", 0),
                isolated_count=len(result.isolated),
                families_1d_count=len(result.families_1d),
                unsupported_count=len(result.unsupported),
                rank_histogram=dict(rank_hist),
                validation_failures=val_fail,
                runtime_seconds=t1 - t0,
                peak_memory_kb=peak / 1024,
            )
        )

    tracemalloc.stop()
    report = {
        "software_version": __version__,
        "git_commit": _git_commit(),
        "records": [asdict(r) for r in records],
    }
    return report


def main(argv: list[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Square peg exact solver benchmark")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-md", type=Path, default=None)
    args = parser.parse_args(argv)

    report = run_benchmark(args.corpus)
    out_json = args.out_json or (
        Path(__file__).resolve().parents[3] / "artifacts" / "benchmark_report.json"
    )
    out_md = args.out_md or (
        Path(__file__).resolve().parents[3] / "artifacts" / "benchmark_report.md"
    )
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Benchmark Report",
        "",
        f"Version: {report['software_version']}",
        f"Commit: {report['git_commit']}",
        "",
    ]
    for rec in report["records"]:
        lines.append(f"## {rec['polygon_hash'][:12]}…")
        lines.append(f"- vertices: {rec['num_vertices']}")
        lines.append(f"- quadruples: {rec['quadruples_examined']}")
        lines.append(f"- isolated: {rec['isolated_count']}")
        lines.append(f"- families 1D: {rec['families_1d_count']}")
        lines.append(f"- unsupported: {rec['unsupported_count']}")
        lines.append(f"- validation failures: {rec['validation_failures']}")
        lines.append(f"- runtime: {rec['runtime_seconds']:.3f}s")
        lines.append("")
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_json} and {out_md}")


if __name__ == "__main__":
    main()
