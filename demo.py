from bonds import flemish_bond, stretcher_bond
from brickifier import brickify
from dependency_graph import brick_list_to_placeable_brick_list
from placer import unstrided_placement_order, optimal_placement_order
from printer import interactive_print_placed_bricks, print_bricks


width = 1.5*3 + 1.25
bond = flemish_bond(8, width)
bricks = brickify(bond, width)
placeable_bricks = brick_list_to_placeable_brick_list(1300.0, 800, bricks)
placement_order = optimal_placement_order(placeable_bricks)

interactive_print_placed_bricks(placeable_bricks, placement_order)
