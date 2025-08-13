# Fns to create the bond patterns. We represent the brick patterns created in this file in the
# simplest way: A list (one for each row, first row being the bottom) of lists of the center of the
# head joints on each row (eg, if you want a stretcher at the start of the row, first element will
# be 215 = 210 + 10/2).

from dataclasses import dataclass
import typing as ty

from constants import STRETCHER_LENGTH, HEADER_LENGTH, HEAD_JOINT_WIDTH
from utils import float_eq

assert HEAD_JOINT_WIDTH/2 == HEAD_JOINT_WIDTH//2, "Head joint width must be divisible by zero, i'm sorry"

@dataclass
class Brick:
    left_x: float
    right_x: float

class CourseBuilder:
    """
    Simplify creating a course of bricks. Specify width of each brick one at a time, and it'll
    automatically add head joint widths between them.
    """
    def __init__(self, length: float) -> None:
        self.bricks: list[Brick] = []
        self.length: float = length

    def next_brick_left_x(self) -> float:
        """The left_x of the next brick that we can place on this course"""
        if len(self.bricks) == 0:
            return 0.0

        return self.bricks[-1].right_x + HEAD_JOINT_WIDTH

    def last_brick_right_x(self) -> float:
        if len(self.bricks) == 0:
            return 0.0

        return self.bricks[-1].right_x

    def add_brick(self, length: float, *, truncate_at_end: bool = False) -> None:
        left_x = self.next_brick_left_x()
        right_x = left_x + length
        if right_x > self.length:
            if truncate_at_end:
                right_x = self.length
            else:
                raise RuntimeError("Tried to add a brick that'd go beyond the full length of the course, and truncate_at_end is not set")
        self.bricks.append(Brick(left_x, right_x))

    def to_bricks(self) -> list[Brick]:
        if abs(self.last_brick_right_x() - self.length) > 0.0001:
            raise RuntimeError("Tried to finalize a CourseBuilder but the last brick doesn't end at the full length of the course")
        return self.bricks

def stretcher_bond(num_rows: int, length: int) -> list[list[Brick]]:
    if not float_eq((length - HEADER_LENGTH - HEAD_JOINT_WIDTH) % (STRETCHER_LENGTH + HEAD_JOINT_WIDTH), 0):
        raise ValueError("Invalid length for stretcher bond. The length must be such that each course consists of stretchers except for one header at an end (ie, (a multiple of 210+10)+100+10)")

    all_bricks: list[list[Brick]] = []
    for row in range(num_rows):
        builder = CourseBuilder(length)
        if row % 2 == 0:
            builder.add_brick(HEADER_LENGTH)

        while builder.last_brick_right_x() < length:
            builder.add_brick(STRETCHER_LENGTH, truncate_at_end=True)
        all_bricks.append(builder.to_bricks())
    return all_bricks

FLEMISH_EDGE_BRICK_WIDTH: ty.Final = 

# there are different methods of handling the corners in a flemish bond; I do the simplest thing and
# assume there are three-quarters length cut bricks at the start of half of the rows, and usual
# full-length stretchers in the others.
def flemish_bond(num_rows: int, width: float) -> list[list[Brick]]:
    if not float_eq((length - ))
    assert abs(width%1.5) < 0.0001, "proper flemish bond needs width to be a multiple of 1.5"

    all_bricks: list[list[Brick]] = []
    for row in range(num_rows):
        row_joints: list[float] = []
        if row % 2 == 0:
            i = 0.75
            is_next_stretch = True
        else:
            i = 1.0
            is_next_stretch = False
        while i < width:
            row_joints.append(i)
            i += 1.0 if is_next_stretch else 0.5
            is_next_stretch = not is_next_stretch
        all_bricks.append(row_joints)
    return all_bricks

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
