import pytest

from squarepeg.rough_area.polygonal_lift import lift_from_curve


@pytest.mark.fast
def test_lift_preserves_partition():
    def line(t):
        return (t, 0.0)

    part = [0.0, 0.25, 0.5, 0.75, 1.0]
    lift = lift_from_curve(line, part)
    assert len(lift.points) == len(part)
