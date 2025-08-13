def float_eq(f1: float, f2: float, epsilon: float = 1e-6) -> bool:
    return abs(f1 - f2) < epsilon
