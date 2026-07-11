from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, model_validator


class CalculationType(str, Enum):
    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def no_zero_divisor(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed")
        return self


class CalculationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    a: float
    b: float
    type: CalculationType
    result: float | None
    user_id: int | None
    created_at: datetime
