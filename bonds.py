# Fns to create the bonds. We represent the brick patterns created in this file in the
# simplest way: A list (one for each row, first row being the bottom) of lists of head joint
# positions (left being 0). All these units are "relative" units as described in the readme.

from utils import float_eq

def stretcher_bond(num_rows: int, width: float) -> list[list[float]]:
    assert float_eq(width%0.5, 0), "proper stretcher bond needs width to be a multiple of 0.5"

    all_joints: list[list[float]] = []
    for row in range(num_rows):
        row_joints: list[float] = []
        i = 0.5 if row % 2 == 0 else 1.0
        while i < width:
            row_joints.append(i)
            i += 1
        all_joints.append(row_joints)
    return all_joints

# there are different methods of handling the corners in a flemish bond; I do the simplest thing and
# assume there are three-quarters length cut bricks at the start of half of the rows, and usual
# headers in the others.
def flemish_bond(num_rows: int, width: float) -> list[list[float]]:
    assert float_eq((width-1.25)%1.5, 0), "proper flemish bond needs width to be 1.25 greater than a multiple of 1.5"

    all_joints: list[list[float]] = []
    for row in range(num_rows):
        row_joints: list[float] = []
        if row % 2 == 0:
            i = 0.5
            is_next_stretch = True
        else:
            i = 0.75
            is_next_stretch = False
        while i < width:
            row_joints.append(i)
            i += 1.0 if is_next_stretch else 0.5
            is_next_stretch = not is_next_stretch
        all_joints.append(row_joints)
    return all_joints

# once again, multiple ways to handle corners. I'll just do three-quarters bricks on the stretcher
# rows.
def cross_bond(num_rows: int, width: float) -> list[list[float]]:
    assert width >= 1.5 and abs((width-1.5)%1.0) < 0.0001, "proper cross bond needs width to be 1.5 plus nonnegative integer"

    all_joints: list[list[float]] = []
    for row in range(num_rows):
        row_joints: list[float] = []
        if row % 2 == 0:
            i = 0.5
            increment = 0.5
        else:
            i = 0.75
            increment = 1.0
        while i < width:
            row_joints.append(i)
            i += increment
        all_joints.append(row_joints)
    return all_joints
