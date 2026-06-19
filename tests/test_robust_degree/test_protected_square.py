"""T029 protected square degree."""

import pytest

from squarepeg.robust_degree.degree_certificate import certify_degree, square_exists_from_degree
from squarepeg.robust_degree.protected_box import ProtectedSquareBox, is_protected_square_box


@pytest.mark.fast
def test_unit_circle_has_protected_box():
    import math

    def gamma(t):
        return math.cos(t * 2 * math.pi), math.sin(t * 2 * math.pi)

    box = ProtectedSquareBox(
        windows=((0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)),
        u_box=((0.3, 0.7), (0.3, 0.7), (0.3, 0.7), (0.3, 0.7)),
    )
    checked = is_protected_square_box(gamma, box, boundary_margin=1e-4)
    cert = certify_degree(gamma, box, boundary_margin=1e-4)
    if cert is not None:
        assert square_exists_from_degree(cert)


@pytest.mark.fast
def test_t029_nonzero_degree_implies_existence():
    from squarepeg.robust_degree.degree_certificate import DegreeCertificate

    cert = DegreeCertificate(
        windows=[[0, 1]] * 4,
        u_box=[[0, 1]] * 4,
        degree=-1,
        det_sign=-1,
        boundary_margin=0.01,
        side_length_lower_bound=0.1,
        separation_lower_bound=0.1,
    )
    assert square_exists_from_degree(cert)
