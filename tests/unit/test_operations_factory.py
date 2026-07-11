import pytest

from app.operations import get_operation


def test_factory_returns_correct_operation_for_each_type():
    assert get_operation("Add")(2, 3) == 5
    assert get_operation("Sub")(10, 4) == 6
    assert get_operation("Multiply")(4, 5) == 20
    assert get_operation("Divide")(10, 2) == 5


def test_factory_rejects_unknown_type():
    with pytest.raises(ValueError):
        get_operation("Banana")


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        get_operation("Divide")(10, 0)
