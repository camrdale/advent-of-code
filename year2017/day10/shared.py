from aoc import log


def tie_knot(lengths: list[int], l: list[int], position: int, skip: int) -> tuple[int, int]:
    """Tie a knot in the list of integers in l, modifying it in place. The final position and skip are returned."""
    list_size: int = len(l)
    for length in lengths:
        end = position + length
        knot = list(reversed(
            l[position:end] +
            (l[:(end % list_size)] if end > list_size else [])))
        
        if end > list_size:
            l[position:] = knot[:(list_size - position)]
            l[:(end % list_size)] = knot[(list_size - position):]
        else:
            l[position:end] = knot[:]

        position = (position + length + skip) % list_size
        skip += 1
        log.log(log.DEBUG, l, length, position, end, skip, list_size, knot)
    return position, skip


def knot_hash(lengths: list[int], list_size: int = 256, repeat: int = 1) -> list[int]:
    l = list(range(list_size))
    position = 0
    skip = 0
    for i in range(repeat):
        position, skip = tie_knot(lengths, l, position, skip)
        log.log(log.INFO, i, l, position, skip)
    return l
