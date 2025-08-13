# convert head joint locations to bricks

from dataclasses import dataclass
import typing as ty

@dataclass
class Brick:
    left_x: float
    right_x: float
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
_FULL_CHAR = '█'
_FIRST_HALF_CHAR = '▌'
_LAST_HALF_CHAR = '▐'
_CHARS_PER_WIDTH = 10.5

def print_bricks(bricks: list[list[Brick]]) -> None:
    for brick_row in reversed(bricks):
        row = ''
        current_char = 0
        for brick in brick_row:
            left_char = brick.left_x * _CHARS_PER_WIDTH
            right_char = brick.right_x * _CHARS_PER_WIDTH

            # handle the first char
            distance_to_left_char = left_char - current_char
            if abs(distance_to_left_char) < 0.0001:
                # brick starts immediately: No special behavior
                pass
            elif abs(distance_to_left_char - 0.5) < 0.0001:
                # brick starts half a block later: Print half char
                row += _LAST_HALF_CHAR
                current_char += 1
            else:
                raise RuntimeError('Illegal distance to left char!')

            num_full_chars = int(right_char - current_char)
            row += _FULL_CHAR * num_full_chars
            current_char += num_full_chars

            remaining_brick_chars = right_char - current_char
            if abs(remaining_brick_chars) < 0.0001:
                # brick is done, and so are we
                pass
            elif abs(remaining_brick_chars - 0.5) < 0.0001:
                # half a brick left
                row += _FIRST_HALF_CHAR
                current_char += 1
            else:
                raise RuntimeError(f'Wrong fraction of brick left at the end: {remaining_brick_chars}')
        print(row)
