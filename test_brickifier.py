from brickifier import brickify, Brick

def test_brickify():
    width = 4.5
    # stretcher bond
    bond = [
        [0.5, 1.5, 2.5, 3.5],
        [1.0, 2.0, 3.0, 4.0],
        [0.5, 1.5, 2.5, 3.5],
    ]
    brick_list = brickify(bond, width)
    assert brick_list == [
        Brick(0.0, 0.5, 0),
        Brick(0.5, 1.5, 0),
        Brick(1.5, 2.5, 0),
        Brick(2.5, 3.5, 0),
        Brick(3.5, 4.5, 0),

        Brick(0.0, 1.0, 1),
        Brick(1.0, 2.0, 1),
        Brick(2.0, 3.0, 1),
        Brick(3.0, 4.0, 1),
        Brick(4.0, 4.5, 1),

        Brick(0.0, 0.5, 2),
        Brick(0.5, 1.5, 2),
        Brick(1.5, 2.5, 2),
        Brick(2.5, 3.5, 2),
        Brick(3.5, 4.5, 2),
    ]

def test_brick_real_x():
    stretcher = Brick(1.0, 2.0, 0)
    assert stretcher.real_left_x() == 220
    assert stretcher.real_right_x() == 430

    header = Brick(1.0, 1.5, 0)
    assert header.real_left_x() == 220
    assert header.real_right_x() == 320

    quarter = Brick(1.0, 1.25, 0)
    assert quarter.real_left_x() == 220
    assert quarter.real_right_x() == 265

    # and just to make sure we handle 0.0 startintg point correctly:
    stretcher_2 = Brick(0.0, 1.0, 0)
    assert stretcher_2.real_left_x() == 0
    assert stretcher_2.real_right_x() == 210
