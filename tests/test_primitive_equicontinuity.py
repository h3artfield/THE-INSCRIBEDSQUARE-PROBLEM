import pytest

from squarepeg.area_variation.adversarial_arcs import all_adversarial
from squarepeg.area_variation.exact_2variation import max_partition_sum_squares
from squarepeg.area_variation.inequality_certificate import SHARP_CANDIDATE
from squarepeg.rough_area.liouville_recovery import recover_primitive


@pytest.mark.fast
def test_primitive_increment_area_bound():
    """|f(t)-f(s)| <= M|x(t)-x(s)| + (pi/4) var2^2 template on adversarial arcs."""
    for name, arc in all_adversarial():
        verts = list(arc.vertices)
        prim = recover_primitive(verts)
        m = max(abs(v[1]) for v in verts) + 1
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                sub = verts[i : j + 1]
                local_sq = max_partition_sum_squares(sub)
                dx = abs(verts[j][0] - verts[i][0])
                bound = m * dx + SHARP_CANDIDATE * local_sq
                assert abs(prim[j] - prim[i]) <= bound + 0.5
