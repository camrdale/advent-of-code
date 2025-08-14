import functools
import operator


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
    return position, skip


def knot_hash(input: str) -> list[int]:
    """Knot hash the given input. The dense hash of 16 bytes is returned."""
    lengths = [ord(c) for c in input] + [17, 31, 73, 47, 23]

    l = list(range(256))
    position = 0
    skip = 0
    for _ in range(64):
        position, skip = tie_knot(lengths, l, position, skip)

    dense_hash: list[int] = [
        functools.reduce(operator.xor, l[i*16:(i+1)*16])
        for i in range(16)]

    return dense_hash
