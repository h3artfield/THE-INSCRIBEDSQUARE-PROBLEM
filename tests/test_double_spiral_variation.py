import pytest

from squarepeg.residual_curves.double_spiral import (
    arm_arc_length,
    one_arm_action,
    two_var_partition_sum,
)


@pytest.mark.fast
def test_arc_length_diverges():
    a0 = arm_arc_length(2 * 3.14159, 50)
    a1 = arm_arc_length(2 * 3.14159, 100)
    assert a1 > a0


@pytest.mark.fast
def test_two_var_sum_grows():
    s10 = two_var_partition_sum(10)
    s20 = two_var_partition_sum(20)
    assert s20 > s10


@pytest.mark.fast
def test_one_arm_action_grows_logarithmically():
    a50 = one_arm_action(2 * 3.14159, 50)
    a100 = one_arm_action(2 * 3.14159, 100)
    assert a100 > a50
