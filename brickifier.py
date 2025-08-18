# convert head joint locations to bricks

from dataclasses import dataclass
import typing as ty

from utils import assert_round

_STRETCHER_WIDTH: ty.Final = 210
_HEAD_JOINT_WIDTH: ty.Final = 10

@dataclass
class Brick:
    relative_left_x: float
    relative_right_x: float
    y: int # course, 0 being the bottom course
    is_placed: bool = False

    # could argue these should be float, but for real quarter/header/stretcher widths in mm for this
    # problem, they'll always be integral.
    def real_left_x(self) -> int:
        return relative_to_real_including_joint(self.relative_left_x)

    def real_right_x(self) -> int:
        return relative_to_real_excluding_joint(self.relative_right_x)

# when constructing a BrickList type, you must also uphold the invariant that the bricks are
# top-to-bottom, left-to-right
BrickList: ty.TypeAlias = list[Brick]

def relative_to_real_including_joint(relative: float) -> int:
    return assert_round(relative*(_STRETCHER_WIDTH + _HEAD_JOINT_WIDTH))

def relative_to_real_excluding_joint(relative: float) -> int:
    return relative_to_real_including_joint(relative) - _HEAD_JOINT_WIDTH

# Takes relative head joint positions on each row, not including the first (0.0) or last (=width)
# positions.
def brickify(all_head_joints: list[list[float]], width: float) -> BrickList:
    result: BrickList = []
    for course_no, head_joints_row in enumerate(all_head_joints):
        last_head_joint = 0.0
        for head_joint in head_joints_row + [width]:
            result.append(Brick(relative_left_x=last_head_joint, relative_right_x=head_joint, y=course_no))
            last_head_joint = head_joint
    return result

# time to overengineer the brick printing mechanism
_PLACED_CHAR: ty.Final = '█'
_UNPLACED_CHAR: ty.Final = '▒'
_HEAD_JOINT_CHAR: ty.Final = ' '
_STRETCHER_PLUS_TRAILING_HEAD_JOINT_LENGTH_CHARS: ty.Final = 8
_HEAD_JOINT_LENGTH_CHARS: ty.Final = 1

def print_bricks(bricks: BrickList) -> None:
    row = ''
    last_y = 0
    last_relative_right_x = 0
    for brick in bricks:
        if brick.y < last_y:
            raise ValueError(f"BrickList invariant violated: decreasing course number (y) from {last_y} to {brick.y}")

        if brick.y > last_y:
            print(row)
            print()

        if brick.y == last_y and brick.relative_left_x != last_relative_right_x:
            raise ValueError(f"BrickList invariant violated: relative left_x {brick.relative_left_x} was not equal to previous right_x {last_relative_right_x} on course {brick.y}")

        last_y = brick.y
        last_relative_right_x = brick.relative_right_x

        # sorry for the name
        brick_plus_trailing_head_joint_length_chars = assert_round((brick.relative_right_x - brick.relative_left_x) * _STRETCHER_PLUS_TRAILING_HEAD_JOINT_LENGTH_CHARS)
        brick_length_chars = brick_plus_trailing_head_joint_length_chars - _HEAD_JOINT_LENGTH_CHARS
        row += _PLACED_CHAR * brick_length_chars
        row += _HEAD_JOINT_CHAR * _HEAD_JOINT_LENGTH_CHARS
