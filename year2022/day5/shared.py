import collections
import re


MOVE = re.compile(r'move ([0-9]*) from ([0-9]*) to ([0-9]*)')


def parse_stacks(crates_input: list[str]) -> dict[int, list[str]]:
    crates: dict[int, list[str]] = collections.defaultdict(list)
    for line in crates_input[-2::-1]:
        i = 1
        while 1+(4*(i-1)) < len(line):
            crate = line[1+(4*(i-1))]
            if crate != ' ':
                crates[i].append(crate)
            i += 1
    return crates


def parse_moves(moves_input: list[str]) -> list[tuple[int,...]]:
    moves: list[tuple[int, ...]] = []
    for line in moves_input:
        match = MOVE.match(line)
        assert match is not None
        moves.append(tuple(map(int, match.groups())))
    return moves
