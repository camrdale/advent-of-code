from collections import Counter, defaultdict
import re


GUARD_LOG = re.compile(r'\[[0-9-]* [0-9]*:([0-9]*)\] (?:Guard #([0-9]*) begins shift|(falls asleep|wakes up))')


def track_guards(input: list[str]) -> dict[int, Counter[int]]:
    guards: dict[int, Counter[int]] = defaultdict(Counter)
    guard = -1
    falls_asleep = 0
    for line in input:
        match = GUARD_LOG.match(line)
        assert match is not None
        if match.group(2) is not None:
            guard = int(match.group(2))
        elif match.group(3) == 'falls asleep':
            falls_asleep = int(match.group(1))
        else:
            wakes_up = int(match.group(1))
            guards[guard].update(range(falls_asleep, wakes_up))
    return guards
