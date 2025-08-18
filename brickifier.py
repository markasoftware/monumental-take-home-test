from dataclasses import dataclass
import typing as ty

from utils import assert_round

_STRETCHER_WIDTH: ty.Final = 210
_HEAD_JOINT_WIDTH: ty.Final = 10
_BRICK_HEIGHT: ty.Final = 50
_BED_JOINT_HEIGHT: ty.Final = 12.5

@dataclass(frozen=True)
class Brick:
    relative_left_x: float
    relative_right_x: float
    course_no: int # course, 0 being the bottom course

    # could argue these should be float, but for real quarter/header/stretcher widths in mm for this
    # problem, they'll always be integral.
    def real_left_x(self) -> int:
        return relative_to_real_including_joint(self.relative_left_x)

    def real_right_x(self) -> int:
        return relative_to_real_excluding_joint(self.relative_right_x)

    def real_bottom_y(self) -> float:
        return self.course_no * (_BRICK_HEIGHT + _BED_JOINT_HEIGHT)

    def real_top_y(self) -> float:
        return self.real_bottom_y() + _BRICK_HEIGHT

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
            result.append(Brick(relative_left_x=last_head_joint, relative_right_x=head_joint, course_no=course_no))
            last_head_joint = head_joint
    return result
