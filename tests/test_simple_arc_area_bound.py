import math

import pytest

from squarepeg.area_variation.adversarial_arcs import all_adversarial, max_ratio_search
from squarepeg.area_variation.inequality_certificate import SHARP_CANDIDATE, certify_arc
from squarepeg.area_variation.adversarial_arcs import semicircle_arc


@pytest.mark.fast
def test_all_adversarial_pass_pi_over_4():
    for name, arc in all_adversarial():
        cert = certify_arc(arc)
        assert cert.passes, f"{name} ratio {cert.ratio}"


@pytest.mark.fast
def test_max_ratio_below_sharp_constant():
    name, ratio, ok = max_ratio_search()
    assert ok
    assert ratio <= SHARP_CANDIDATE + 1e-6


@pytest.mark.fast
def test_semicircle_ratio_is_pi_over_8():
    arc = semicircle_arc(128)
    cert = certify_arc(arc)
    assert cert.ratio == pytest.approx(math.pi / 8, rel=0.01)
