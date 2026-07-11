import pytest
from pydantic import ValidationError

from app.schemas.calculation import CalculationCreate, CalculationRead


def test_create_accepts_valid_input():
    calc = CalculationCreate(a=2, b=3, type="Add")
    assert calc.type == "Add"


def test_create_rejects_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=2, b=3, type="Banana")


def test_create_rejects_zero_divisor():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="Divide")


def test_create_allows_zero_b_for_non_divide():
    calc = CalculationCreate(a=10, b=0, type="Multiply")
    assert calc.b == 0


def test_create_rejects_non_numeric_operand():
    with pytest.raises(ValidationError):
        CalculationCreate(a="hello", b=3, type="Add")


def test_read_serializes_from_model_attributes():
    assert "result" in CalculationRead.model_fields
    assert "user_id" in CalculationRead.model_fields
