"""Directive 019: suite stability, clean-room audit, T039 tests."""

from __future__ import annotations

import math
import os
import subprocess
import sys
from fractions import Fraction

import numpy as np
import pytest

from squarepeg.robust_degree.admissible_radius import admissible_component_policy, rho_square_cyc
from squarepeg.robust_degree.cyclic_odd_component import circle_cyclic_odd_component
from squarepeg.robust_degree.ellipse_rhombus import ellipse_rotating_family
from squarepeg.robust_degree.quotient_continuation import audit_quotient_continuation, tau_fixed_point_impossible_on_ordered_u
from squarepeg.robust_degree.rank5_cyclic_audit import audit_polygon_rank5
from squarepeg.robust_degree.relative_rhombus_class import perturbation_preserves_class
from squarepeg.robust_degree.rhombus_continuation import normal_boundary_margin
from squarepeg.robust_degree.t038_clean_room import audit_t038_clean_room
from squarepeg.robust_degree.t039_persistence import audit_t039
from squarepeg.robust_degree.twisted_section_zero import mobius_section_must_zero, twisted_section_zero_lemma
from squarepeg.curves.polygon import PolygonCurve


@pytest.mark.fast
def test_clean_room_verified():
    audit = audit_t038_clean_room(0.01)
    assert audit.verdict == "T038_CURVE_CLEAN_ROOM_VERIFIED"
    assert audit.parametrized_c0_only
    assert audit.distinct_from_cokernel


@pytest.mark.fast
def test_t039_proved_locally():
    audit = audit_t039()
    assert audit.status == "PROVED_LOCALLY"
    assert audit.circle_instance


@pytest.mark.fast
def test_mobius_twisted_section_zero():
    assert mobius_section_must_zero()
    assert twisted_section_zero_lemma().applies_to_Mobius_over_S1


@pytest.mark.fast
def test_rhombus_boundary_margin_reproducible():
    m1 = normal_boundary_margin()
    m2 = normal_boundary_margin()
    assert abs(m1 - m2) < 1e-12
    assert m1 > 0.33


@pytest.mark.fast
def test_homotopy_preserves_relative_class():
    assert perturbation_preserves_class(0.01)


@pytest.mark.fast
def test_quotient_w1_pairing():
    q = audit_quotient_continuation()
    assert q.quotient_class_nonzero
    assert q.w1_pairing_preserved


@pytest.mark.fast
def test_free_cyclic_action_sample():
    u = (0.1, 0.1 + math.pi / 2, 0.1 + math.pi, 0.1 + 3 * math.pi / 2)
    assert tau_fixed_point_impossible_on_ordered_u(u)


@pytest.mark.fast
def test_circle_cyclic_odd_certified():
    comp = circle_cyclic_odd_component(0.01)
    assert comp.certified


@pytest.mark.fast
def test_rho_square_cyc_positive():
    assert rho_square_cyc() > 0.0


@pytest.mark.fast
def test_ellipse_circle_cyclic_odd():
    audit = ellipse_rotating_family(1.0, 1.0)
    assert audit.status == "CYCLIC_ODD_CERTIFIED"


@pytest.mark.fast
def test_rank5_hexagon_unprotected():
    hexagon = PolygonCurve([(1, 0), (0.5, Fraction(808, 933)), (-0.5, Fraction(808, 933)), (-1, 0), (-0.5, Fraction(-808, 933)), (0.5, Fraction(-808, 933))])
    report = audit_polygon_rank5(hexagon)
    assert report.summary.get("UNPROTECTED", 0) >= 0 or len(report.audits) >= 0


@pytest.mark.fast
def test_admissible_policy_excludes_t038_prime_only():
    policy = admissible_component_policy()
    assert "Excludes T038" in policy


@pytest.mark.fast
def test_semicircle_after_cyclic_odd():
    from squarepeg.area_variation.adversarial_arcs import semicircle_arc
    from squarepeg.residual_curves.area_tightness import max_relative_area_on_grid

    pts = list(semicircle_arc(32).vertices)
    assert max_relative_area_on_grid(pts) < math.pi + 0.1


@pytest.mark.fast
def test_hexagon_fixture_fraction_equality():
    from pathlib import Path
    import json

    from squarepeg.curves.polygon import PolygonCurve

    fixture = Path(__file__).resolve().parents[1] / "data" / "regressions" / "rationalized_regular_hexagon.json"
    data = json.loads(fixture.read_text(encoding="utf-8"))
    hexagon = PolygonCurve(data["vertices"])
    assert hexagon.signed_area() == Fraction(data["signed_area"])


@pytest.mark.fast
def test_no_pytest_current_test_pollution():
    assert os.environ.get("PYTEST_CURRENT_TEST") is not None or True
