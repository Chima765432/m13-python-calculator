def add(a: float, b: float) -> float:
    return a + b


def sub(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


OPERATIONS = {
    "Add": add,
    "Sub": sub,
    "Multiply": multiply,
    "Divide": divide,
}


def get_operation(type_name: str):
    try:
        return OPERATIONS[type_name]
    except KeyError:
        raise ValueError(f"Unknown calculation type: {type_name}")
