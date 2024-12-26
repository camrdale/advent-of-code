from collections import Counter
import itertools

from aoc.log import log, RESULT


def vents(input: list[str], consider_diagonals: bool):
    # Multiset of (x,y) coords counting the number of vents that overlap there.
    counts: Counter[tuple[int, int]] = Counter()

    for line in input:
        pieces = line.split()
        x1, y1 = tuple(int(i) for i in pieces[0].split(','))
        x2, y2 = tuple(int(i) for i in pieces[2].split(','))

        if not consider_diagonals and x1 != x2 and y1 != y2:
            # Consider only horizontal and vertical lines.
            continue

        if x1 == x2:
            x_range = itertools.repeat(x1, abs(y1 - y2) + 1)
        else:
            x_step = -1 if x1 > x2 else 1
            x_range = range(x1, x2 + x_step, x_step)

        if y1 == y2:
            y_range = itertools.repeat(y1, abs(x1 - x2) + 1)
        else:
            y_step = -1 if y1 > y2 else 1
            y_range = range(y1, y2 + y_step, y_step)

        counts.update(zip(x_range, y_range))

    overlapping_vents = sum(1 for _, cnt in counts.items() if cnt >= 2)
    log(RESULT, 'Number of locations with 2 or more overlapping vents:', overlapping_vents)
    return overlapping_vents
