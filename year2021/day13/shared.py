import re

from aoc.map import Coordinate


FOLD = re.compile(r'fold along (x|y)=([0-9]*)')


def fold(dots: set[Coordinate], fold_input: str) -> set[Coordinate]:
    match = FOLD.match(fold_input)
    assert match is not None
    direction = match.group(1)
    fold_line = int(match.group(2))

    folded_dots: set[Coordinate] = set()

    for dot in dots:
        if direction == 'x' and dot.x > fold_line:
            dot = dot._replace(x=(2*fold_line - dot.x))
        elif direction == 'y' and dot.y > fold_line:
            dot = dot._replace(y=(2*fold_line - dot.y))
        folded_dots.add(dot)

    return folded_dots
