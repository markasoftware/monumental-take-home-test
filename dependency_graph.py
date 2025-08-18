from __future__ import annotations

import typing as ty

from dataclasses import dataclass
from brickifier import Brick, BrickList

@dataclass
class PlaceableBrick:
    brick: Brick
    dependencies: list[PlaceableBrick]
    within_same_stride: list[PlaceableBrick]
    # if int, indicates which stride the brick was placed in. If None, the brick hasn't been placed
    # yet.
    placed_in_stride: int | None = None

    def __hash__(self) -> int:
        return hash(self.brick)

PlaceableBrickList: ty.TypeAlias = list[PlaceableBrick]

def brick_list_to_placeable_brick_list(stride_height: float, stride_width: int, brick_list: BrickList) -> PlaceableBrickList:
    """
    Computes dependencies between bricks and suchlike. Returns bricks in same order as passed in.
    """
    # for this interview take-home, performance frankly doesn't matter much so we'll do an awful
    # brute-force O(n^2) both for determining dependencies between bricks and for computing which
    # bricks can be within the same block

    # TODO explain how it can be made faster

    placeable_brick_list = [PlaceableBrick(brick, [], []) for brick in brick_list]
    for placeable_brick in placeable_brick_list:
        # find dependencies
        brick = placeable_brick.brick
        for other_placeable_brick in placeable_brick_list:
            other_brick = other_placeable_brick.brick
            if brick.course_no - 1 == other_brick.course_no and do_bricks_overlap(brick, other_brick):
                placeable_brick.dependencies.append(other_placeable_brick)
            if are_bricks_in_same_stride(stride_height, stride_width, brick, other_brick):
                placeable_brick.within_same_stride.append(other_placeable_brick)

    return placeable_brick_list

def do_bricks_overlap(brick: Brick, other_brick: Brick) -> bool:
    """Return whether the real x ranges of the two bricks overlap at all"""
    # this max/min construction is the intersection range of the two bricks' real x ranges
    intersection_left_x = max(brick.real_left_x(), other_brick.real_left_x())
    intersection_right_x = min(brick.real_right_x(), other_brick.real_right_x())
    # if the intersection is a valid interval, then they overlap
    return intersection_left_x <= intersection_right_x

# There's potentially more nuance to the definition of a window than this based on how the mortar
# for head joints works.
def are_bricks_in_same_stride(stride_height: float, stride_width: int, brick: Brick, other_brick: Brick):
    """
    Determine whether the bricks are within `stride_height` mm vertically and `window_width` mm
    horizontally.
    """
    vertical_distance = max(brick.real_top_y(), other_brick.real_top_y()) - min(brick.real_bottom_y(), other_brick.real_bottom_y())
    horizontal_distance = max(brick.real_right_x(), other_brick.real_right_x()) - min(brick.real_left_x(), other_brick.real_left_x())
    return vertical_distance <= stride_height and horizontal_distance <= stride_width
