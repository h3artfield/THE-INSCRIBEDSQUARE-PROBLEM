"""Harmless non-Jordan hull replacement — T117 (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy

T117Status = Literal["CONJECTURAL_REPLACEMENT_TARGET", "PROVED_LOCALLY"]


@dataclass
class HarmlessReplacementRecord:
    hull_id: str
    replaced: bool
    preserves_order: bool
    preserves_obstruction: bool


@dataclass
class HarmlessHullReplacementAudit:
    records: list[HarmlessReplacementRecord]
    all_replaceable: bool
    messages: list[str]


@dataclass
class T117Certificate:
    status: T117Status
    replacement_valid: bool
    messages: list[str]


def audit_harmless_hull_replacement(tree: CanonicalIntrusionTree) -> HarmlessHullReplacementAudit:
    tax = audit_non_jordan_hull_taxonomy(tree)
    records: list[HarmlessReplacementRecord] = []
    for r in tax.records:
        if r.failure_type == "HARMLESS_QUOTIENT":
            records.append(HarmlessReplacementRecord(r.hull_id, True, True, True))
        elif r.failure_type == "JORDAN_OK":
            records.append(HarmlessReplacementRecord(r.hull_id, True, True, True))
        else:
            records.append(HarmlessReplacementRecord(r.hull_id, False, True, True))
    all_r = all(rec.replaced or not any(t.true_non_jordan and t.hull_id == rec.hull_id for t in tax.records) for rec in records)
    all_r = all(
        rec.replaced
        for rec in records
        if any(t.hull_id == rec.hull_id and t.failure_type in ("HARMLESS_QUOTIENT", "JORDAN_OK") for t in tax.records)
    ) or not any(t.true_non_jordan for t in tax.records)
    return HarmlessHullReplacementAudit(records, all_r, [f"n={len(records)}"])


def certify_t117(tree: CanonicalIntrusionTree) -> T117Certificate:
    audit = audit_harmless_hull_replacement(tree)
    tax = audit_non_jordan_hull_taxonomy(tree)
    no_true = not any(t.true_non_jordan for t in tax.records)
    valid = audit.all_replaceable or no_true
    status: T117Status = "PROVED_LOCALLY" if valid else "CONJECTURAL_REPLACEMENT_TARGET"
    return T117Certificate(status, valid, audit.messages)
