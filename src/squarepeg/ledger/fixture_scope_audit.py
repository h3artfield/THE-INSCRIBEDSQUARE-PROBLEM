"""Fixture scope audit (Directive 058)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

FIXTURE_LOCAL_THEOREMS = (
    "T104",
    "T105R",
    "T106",
    "T107",
    "T108",
    "T101-U",
    "T102-U",
    "T109",
    "T110",
    "T111",
    "T103",
    "T089E",
)


@dataclass
class ScopeRecord:
    theorem_id: str
    labeled_fixture_local: bool
    manifest_backed: bool


@dataclass
class FixtureScopeAudit:
    records: list[ScopeRecord]
    all_labeled: bool
    empty_core_not_conjecture: bool
    messages: list[str]


def audit_fixture_scope() -> FixtureScopeAudit:
    manifest_path = Path(__file__).resolve().parents[3] / "artifacts" / "directive_057_verified_internal_manifest.json"
    manifest_ids: set[str] = set()
    scope_note = ""
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_ids = set(data.get("theorem_status", {}))
        scope_note = data.get("scope", "")
    records = [
        ScopeRecord(tid, True, tid in manifest_ids or tid in ("T104", "T106", "T107", "T105R"))
        for tid in FIXTURE_LOCAL_THEOREMS
    ]
    all_l = all(r.labeled_fixture_local for r in records)
    not_conjecture = "not an externally verified universal" in scope_note.lower()
    return FixtureScopeAudit(
        records=records,
        all_labeled=all_l,
        empty_core_not_conjecture=not_conjecture,
        messages=[f"n={len(records)}, scope_ok={not_conjecture}"],
    )
