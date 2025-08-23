import typing as ty

from dependency_graph import PlaceableBrickList
from placer import PlacementOrder, apply_placement_order
from utils import assert_round

_PLACED_CHAR: ty.Final = '█'
_UNPLACED_CHAR: ty.Final = '▒'
_HEAD_JOINT_CHAR: ty.Final = ' '
_STRETCHER_PLUS_TRAILING_HEAD_JOINT_LENGTH_CHARS: ty.Final = 8
_HEAD_JOINT_LENGTH_CHARS: ty.Final = 1

def colorize(text: str, color_id: int) -> str:
    # chatgpt generated this color list, idk if these labels are actually right
    palette = [
        196,  # vivid red
        208,  # orange
        226,  # yellow
        46,   # green
        51,   # cyan
        27,   # deep blue
        201,  # hot pink/magenta
        93,   # purple/violet
        118,  # lime
        39,   # sky blue
    ]

    color_code = (palette[color_id % len(palette)] + 10 * (color_id // len(palette))) % 256
    start = f"\x1b[38;5;{color_code}m"
    end = "\x1b[0m"
    return f"{start}{text}{end}"

def print_bricks(placeable_bricks: PlaceableBrickList) -> None:
    rows: list[str] = []
    row = ''
    last_y = 0
    last_relative_right_x = 0
    for placeable_brick in placeable_bricks:
        brick = placeable_brick.brick
        if brick.course_no < last_y:
            raise ValueError(f"BrickList invariant violated: decreasing course number (y) from {last_y} to {brick.course_no}")

        if brick.course_no > last_y:
            rows.append(row)
            row = ''

        if brick.course_no == last_y and brick.relative_left_x != last_relative_right_x:
            raise ValueError(f"BrickList invariant violated: relative left_x {brick.relative_left_x} was not equal to previous right_x {last_relative_right_x} on course {brick.course_no}")

        last_y = brick.course_no
        last_relative_right_x = brick.relative_right_x

        # sorry for the name
        brick_plus_trailing_head_joint_length_chars = assert_round((brick.relative_right_x - brick.relative_left_x) * _STRETCHER_PLUS_TRAILING_HEAD_JOINT_LENGTH_CHARS)
        brick_length_chars = brick_plus_trailing_head_joint_length_chars - _HEAD_JOINT_LENGTH_CHARS
        if placeable_brick.placed_in_stride is not None:
            row += colorize(_PLACED_CHAR * brick_length_chars, placeable_brick.placed_in_stride)
        else:
            row += _UNPLACED_CHAR * brick_length_chars
        row += _HEAD_JOINT_CHAR * _HEAD_JOINT_LENGTH_CHARS

    rows.append(row)
    for rev_row in reversed(rows):
        print(rev_row)
        print()

def interactive_print_placed_bricks(placeable_bricks: PlaceableBrickList, placement_order: PlacementOrder) -> None:
    """
    Print the brick list, and then every time the user presses enter, place one more brick according
    to the placement order and print again. Terminates once the placement order is exhausted.
    Mutates `placeable_bricks`.
    """
    print_bricks(placeable_bricks)
    for _ in apply_placement_order(placement_order):
        _ = input("Press enter to place the next brick")
        print_bricks(placeable_bricks)
