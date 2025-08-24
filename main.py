import argparse
from datetime import timedelta

from bonds import flemish_bond, stretcher_bond, cross_bond, wild_bond
from brickifier import brickify
from dependency_graph import brick_list_to_placeable_brick_list
from placer import apply_placement_order, optimal_placement_order
from printer import interactive_print_placed_bricks, print_bricks


def main():
    parser = argparse.ArgumentParser(description="Brick placement simulator.")
    parser.add_argument(
        '--bond',
        type=str,
        default='stretcher',
        choices=['stretcher', 'flemish', 'cross', 'wild'],
        help='Bond pattern',
    )
    parser.add_argument('--num-courses', type=int, default=10, help='Number of courses (rows).')
    parser.add_argument(
        '--width',
        type=float,
        help='Width of the wall in stretchers (relative units). If not provided, a default will be used based on the bond type.'
    )
    parser.add_argument('--stride-height', type=float, default=1300.0, help='Stride height in mm')
    parser.add_argument('--stride-width', type=int, default=800, help='Stride width in mm')
    parser.add_argument('--time-limit', type=int, default=20, help='Time limit in seconds for optimal placement order computation.')
    parser.add_argument(
        '--instant',
        action='store_true',
        help='Print the final colors instead of placing bricks one-by-one with ENTER',
    )

    args = parser.parse_args()

    width = args.width
    if width is None:
        if args.bond == 'stretcher':
            width = 5.0  # multiple of 0.5
        elif args.bond == 'flemish':
            width = 1.5 * 3 + 1.25  # 5.75, satisfies (width-1.25)%1.5 == 0
        elif args.bond == 'cross':
            width = 1.5 + 4.0  # 5.5, satisfies (width-1.5)%1.0 == 0
        elif args.bond == 'wild':
            width = 5.0  # multiple of 0.25

    bond_fn_map = {
        'stretcher': stretcher_bond,
        'flemish': flemish_bond,
        'cross': cross_bond,
        'wild': wild_bond,
    }
    bond_fn = bond_fn_map[args.bond]
    bond = bond_fn(args.num_courses, width)

    bricks = brickify(bond, width)
    placeable_bricks = brick_list_to_placeable_brick_list(args.stride_height, args.stride_width, bricks)
    placement_order = optimal_placement_order(placeable_bricks, time_limit=timedelta(seconds=args.time_limit))

    if args.instant:
        for _ in apply_placement_order(placement_order):
            pass
        print_bricks(placeable_bricks)
    else:
        interactive_print_placed_bricks(placeable_bricks, placement_order)


if __name__ == "__main__":
    main()
