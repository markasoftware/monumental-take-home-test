from bonds import Brick, stretcher_bond, flemish_bond

def test_stretcher_bond() -> None:
    bond = stretcher_bond(3, 220*4 + 120)
    header_first_course = [
        # start with header, all rest stretchers:
        Brick(0.0, 110.0),
        Brick(120.0, 330.0),
        Brick(340.0, 550.0),
        Brick(560.0, 770.0),
        Brick(780.0, 990.0),
    ]
    header_last_course = [
        Brick(0.0, 210.0),
        Brick(220.0, 430.0),
        Brick(440.0, 650.0),
        Brick(660.0, 870.0),
        # end with header, all rest stretchers:
        Brick(880.0, 990.0),
    ]
        
    assert bond == [
        header_first_course,
        header_last_course,
        header_first_course,
    ]

def test_flemish_bond() -> None:
    bond = 
