from bonds import stretcher_bond, flemish_bond, cross_bond

def test_stretcher_bond() -> None:
    bond = stretcher_bond(3, 4.5)
    first_course = [0.5, 1.5, 2.5, 3.5]
    second_course = [1.0, 2.0, 3.0, 4.0]

    # there really shoul be exact float equality here, everything is just halves
    assert bond == [
        first_course,
        second_course,
        first_course,
    ]

def test_flemish_bond() -> None:
    bond = flemish_bond(3, 5.75)
    first_course = [0.5, 1.5, 2.0, 3.0, 3.5, 4.5, 5.0]
    second_course = [0.75, 1.25, 2.25, 2.75, 3.75, 4.25, 5.25]

    assert bond == [
        first_course,
        second_course,
        first_course,
    ]

def test_cross_bond() -> None:
    bond = cross_bond(3, 4.5)
    first_course = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    second_course = [0.75, 1.75, 2.75, 3.75]

    assert bond == [
        first_course,
        second_course,
        first_course,
    ]
