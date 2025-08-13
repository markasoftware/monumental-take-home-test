# convert head joint locations to bricks

from dataclasses import dataclass
import typing as ty

from utils import assert_round

@dataclass
class Brick:
    relative_left_x: float
    relative_right_x: float
    # could argue these should be float, but for real quarter/header/stretcher widths in mm for this
    # problem, they'll always be integral.
    real_left_x: int
    real_right_x: int
    y: int # course, 0 being the bottom course
    is_placed: bool = False

_HEAD_JOINT_WIDTH = 1.0/21.0

def _single_row_joints_to_bricks(joints: list[float], width: float) -> list[Brick]:
    result: list[Brick] = []
    prev_x = 0.0
    for joint in joints:
        result.append(Brick(left_x = prev_x, right_x = joint - _HEAD_JOINT_WIDTH/2))
        prev_x = joint + _HEAD_JOINT_WIDTH/2
    result.append(Brick(left_x = prev_x, right_x = width))
    return result

def head_joints_to_bricks(joints: list[list[float]], width: float) -> list[list[Brick]]:
    return [_single_row_joints_to_bricks(row_joints, width) for row_joints in joints]

# time to overengineer the brick printing mechanism
_PLACED_CHAR: ty.Final = '█'
_UNPLACED_CHAR: ty.Final = '▒'
_HEAD_JOINT_CHAR: ty.Final = ' '
_STRETCHER_PLUS_TRAILING_HEAD_JOINT_LENGTH_CHARS: ty.Final = 8
_HEAD_JOINT_LENGTH_CHARS: ty.Final = 1

def print_bricks(head_joints: list[list[float]], length: float) -> None:
    for head_joint_row in reversed(head_joints):
        row = ''
        prev_head_joint = 0.0
        for head_joint in head_joint_row + [length]:
            # sorry for the name
            brick_plus_trailing_head_joint_length_chars = assert_round((head_joint - prev_head_joint) * _STRETCHER_PLUS_TRAILING_HEAD_JOINT_LENGTH_CHARS)
            brick_length_chars = brick_plus_trailing_head_joint_length_chars - _HEAD_JOINT_LENGTH_CHARS
            row += _PLACED_CHAR * brick_length_chars
            row += _HEAD_JOINT_CHAR * _HEAD_JOINT_LENGTH_CHARS
            prev_head_joint = head_joint
        print(row)
        print()
