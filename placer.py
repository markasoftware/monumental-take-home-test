from datetime import timedelta
import minizinc

from collections import defaultdict
import collections.abc as tyc
from math import ceil
import time
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

def optimal_placement_order(placeable_brick_list: PlaceableBrickList, time_limit: timedelta) -> PlacementOrder:
    """
    Compute the optimal, multi-stride brick placement order using a discrete optimizer (effectively
    a SAT solver)
    """
    # Adjacency matrix of dependencies. Set [i][j] if brick i depends on brick j
    dependency_matrix: list[list[bool]] = [
        [
            i_placeable_brick in j_placeable_brick.dependencies
            for j_placeable_brick in placeable_brick_list
        ]
        for i_placeable_brick in placeable_brick_list
    ]
    same_stride_matrix: list[list[bool]] = [
        [
            j_placeable_brick in i_placeable_brick.within_same_stride
            for j_placeable_brick in placeable_brick_list
        ]
        for i_placeable_brick in placeable_brick_list
    ]
    model = minizinc.Model("strides.mzn")
    # solver = minizinc.Solver.lookup("gecode")
    # let's try a different one:
    solver = minizinc.Solver.lookup("gecode")
    instance = minizinc.Instance(solver, model)
    instance['n_bricks'] = len(placeable_brick_list)
    instance['dependency'] = dependency_matrix
    instance['within_stride'] = same_stride_matrix

    print("Running solver...")
    start_time = time.time()
    result = instance.solve(processes=12, time_limit=time_limit, statistics=True)
    end_time = time.time()
    print(f"Solver finished in {end_time - start_time:.2f} seconds with status {result.status}")

    if result.status != minizinc.result.Status.OPTIMAL_SOLUTION:
        print("WARNING: Solver did not find an optimal solution in time, using best found solution")
    if result.status != minizinc.result.Status.SATISFIED and result.status != minizinc.result.Status.OPTIMAL_SOLUTION:
        raise ValueError("Solver failed to find any solution in time, increase the time limit!")

    stride = result['stride']
    # the stride array is an array of which stride number each brick is in. We want to invert this to a list of lists
    placement_order: PlacementOrder = [[] for _ in range(max(stride) + 1)]
    for i, stride_no in enumerate(stride):
        placement_order[stride_no].append(placeable_brick_list[i])
    # within each stride, we still need to do a topo sort to get a valid ordering
    for i in range(len(placement_order)):
        placement_order[i] = _topo_sort(set(placement_order[i]))
    print(f"Number of strides: {len(placement_order)}")
    return placement_order

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
