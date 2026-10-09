"""Pytest configuration for regression tiers."""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "audit: manifest and frozen snapshot consistency (tier 2)")
    config.addinivalue_line("markers", "deep: sampled deep regression — heavy directive audits (tier 3)")
    config.addinivalue_line("markers", "milestone: full milestone gate — run before tag (tier 4)")
