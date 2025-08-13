def float_eq(f1: float, f2: float, epsilon: float = 1e-6) -> bool:
    return abs(f1 - f2) < epsilon

def assert_round(f: float) -> int:
    result = round(f)
    if not float_eq(float(result), f):
        raise ValueError(f"assert_round argument wasn't near an integer: {f}")
    return result
