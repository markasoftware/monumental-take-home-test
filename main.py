import argparse
from datetime import timedelta

from bonds import flemish_bond, stretcher_bond, cross_bond
from brickifier import brickify
from dependency_graph import brick_list_to_placeable_brick_list
from placer import optimal_placement_order
from printer import interactive_print_placed_bricks


def main():
    parser = argparse.ArgumentParser(description="Brick placement simulator.")
    parser.add_argument(
        '--bond',
        type=str,
        required=True,
        choices=['stretcher', 'flemish', 'cross'],
        help='Type of bond pattern.'
    )
    parser.add_argument('--num-rows', type=int, required=True, help='Number of rows of bricks.')
    parser.add_argument(
        '--width',
        type=float,
        help='Width of the wall. If not provided, a default will be used based on the bond type.'
    )
    parser.add_argument('--stride-height', type=float, default=1300.0, help='Stride height for placement.')
    parser.add_argument('--stride-width', type=int, default=800, help='Stride width for placement.')
    parser.add_argument('--time-limit', type=int, default=10, help='Time limit in seconds for optimal placement order computation.')

    args = parser.parse_args()

    width = args.width
    if width is None:
        if args.bond == 'stretcher':
            width = 3.5  # multiple of 0.5
        elif args.bond == 'flemish':
            width = 1.5 * 3 + 1.25  # 5.75, satisfies (width-1.25)%1.5 == 0
        elif args.bond == 'cross':
            width = 1.5 + 2.0  # 3.5, satisfies (width-1.5)%1.0 == 0

    bond_fn_map = {
        'stretcher': stretcher_bond,
        'flemish': flemish_bond,
        'cross': cross_bond,
    }
    bond_fn = bond_fn_map[args.bond]
    bond = bond_fn(args.num_rows, width)

    bricks = brickify(bond, width)
    placeable_bricks = brick_list_to_placeable_brick_list(args.stride_height, args.stride_width, bricks)
    placement_order = optimal_placement_order(placeable_bricks, time_limit=timedelta(seconds=args.time_limit))

    interactive_print_placed_bricks(placeable_bricks, placement_order)


if __name__ == "__main__":
    main()
