from collections import defaultdict
import collections.abc as tyc
import typing as ty

from dependency_graph import PlaceableBrick, PlaceableBrickList

_STRIDE_HEIGHT: ty.Final = 1300.0
_STRIDE_WIDTH: ty.Final = 800

# Each element of the outer list is a stride, and a stride is the ordering of the bricks to be
# placed within that stride.
PlacementOrder: ty.TypeAlias = list[list[PlaceableBrick]]

# not how we don't use PlaceableBrickList here because the return val is probably not in the usual
# order
def _topo_sort(placeable_bricks: set[PlaceableBrick]) -> list[PlaceableBrick]:
    deps_hash = {
        placeable_brick: {dep for dep in placeable_brick.dependencies if dep in placeable_bricks}
        for placeable_brick in placeable_bricks
    }
    rev_deps_hash: defaultdict[PlaceableBrick, list[PlaceableBrick]] = defaultdict(list)
    for placeable_brick, deps in deps_hash.items():
        for dep in deps:
            rev_deps_hash[dep].append(placeable_brick)

    # to make the order maybe a little more realistic for a robot, prefer the brick closest to the
    # placement head rather than an arbitrary topo order.
    head_x = 0
    head_y = 0

    def sq_distance(placeable_brick: PlaceableBrick) -> float:
        brick = placeable_brick.brick
        mid_x = (brick.real_left_x() + brick.real_right_x()) / 2
        mid_y = (brick.real_top_y() + brick.real_bottom_y()) / 2
        return (mid_x - head_x) ** 2 + (mid_y - head_y) ** 2

    result: list[PlaceableBrick] = []

    # this is a run-of-the-mill topo sort with the tie breaking described above
    while len(deps_hash) > 0:
        immediately_placeable_bricks = (placeable_brick for placeable_brick, deps in deps_hash.items() if len(deps) == 0)
        closest_immediately_placeable_brick: PlaceableBrick | None = None
        for immediately_placeable_brick in immediately_placeable_bricks:
            if closest_immediately_placeable_brick is None or sq_distance(immediately_placeable_brick) < sq_distance(closest_immediately_placeable_brick):
                closest_immediately_placeable_brick = immediately_placeable_brick

        if closest_immediately_placeable_brick is None:
            raise ValueError("Tried to topo sort a cyclic graph")
        del deps_hash[closest_immediately_placeable_brick]
        for rev_dep in rev_deps_hash[closest_immediately_placeable_brick]:
            if rev_dep in deps_hash:
                deps_hash[rev_dep].remove(closest_immediately_placeable_brick)

        result.append(closest_immediately_placeable_brick)

    return result

def unstrided_placement_order(placeable_brick_list: PlaceableBrickList) -> PlacementOrder:
    """Place all the bricks in a single stride"""
    return [_topo_sort(set(placeable_brick_list))]

def apply_placement_order(placement_order: PlacementOrder) -> tyc.Iterator[None]:
    """
    A generator that doesn't actually return anything but instead places one brick every time it's
    called. Will mutate the `PlaceableBrick`s referenced in the `placement_order`
    """
    for i, stride in enumerate(placement_order):
        for placeable_brick in stride:
            if placeable_brick.placed_in_stride is not None:
                raise ValueError("A PlaceableBrick referenced by this PlacementOrder was already placed")
            placeable_brick.placed_in_stride = i
            yield
