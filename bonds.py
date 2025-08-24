# Fns to create the bonds. We represent the brick patterns created in this file in the
# simplest way: A list (one for each row, first row being the bottom) of lists of head joint
# positions (left being 0). All these units are "relative" units as described in the readme.

import minizinc

from datetime import timedelta
import time

def stretcher_bond(num_rows: int, width: float) -> list[list[float]]:
    # exact equality is more or less ok here because 0.5 can be represented exactly as a float.
    # Similarly with 0.25 used in other bonds later
    assert width%0.5 == 0, "proper stretcher bond needs width to be a multiple of 0.5"

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
    assert (width-1.25)%1.5 == 0, "proper flemish bond needs width to be 1.25 greater than a multiple of 1.5"

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
    assert width >= 1.5 and (width-1.5)%1.0 == 0, "proper cross bond needs width to be 1.5 plus nonnegative integer"

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

def wild_bond(num_rows: int, width: float) -> list[list[float]]:
    assert width % 0.25 == 0 and width >= 0.5, "proper wild bond width must be a multiple of 0.25 and at least 0.5"

    model = minizinc.Model("wild.mzn")
    solver = minizinc.Solver.lookup("cp")
    instance = minizinc.Instance(solver, model)
    instance['n_courses'] = num_rows
    instance['width_in_quarters'] = int(width * 4)

    print("Running wild bond solver...")
    start_time = time.time()
    # TODO processes and time_limit as parameters
    result = instance.solve()
    end_time = time.time()
    print(f"Wild bond solved in {end_time - start_time:.2f} seconds with status {result.status}")
    if result.status != minizinc.result.Status.SATISFIED:
        raise ValueError("Wild bond solver failed to find a solution!")

    return [[quarters / 4.0 + 0.25 for quarters, has_joint in enumerate(course) if has_joint] for course in result['head_joints']]
