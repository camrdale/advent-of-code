import collections
import itertools
import re

from aoc import log


HAPPINESS = re.compile(r'(.*) would (gain|lose) ([0-9]*) happiness units by sitting next to (.*)\.')


class SeatingArranger:
    def __init__(self, input: list[str]) -> None:
        self.guests: set[str] = set()
        self.happiness_change: dict[frozenset[str], int] = collections.defaultdict(int)
        for line in input:
            happiness = HAPPINESS.match(line)
            assert happiness is not None, line
            guest_pair = frozenset([happiness.group(1), happiness.group(4)])
            self.guests.update(guest_pair)
            change = int(happiness.group(3)) * (-1 if happiness.group(2) == 'lose' else 1)
            self.happiness_change[guest_pair] += change

    def optimal_arrangement(self) -> int:
        # Head guest sits at the head of the table.
        head = next(iter(self.guests))
        remaining = self.guests - {head}

        best_arrangement = 0
        for guest_order in itertools.permutations(remaining):
            if guest_order[0] < guest_order[-1]:
                # Skip identical arrangements in reverse order
                continue
            arrangement = sum(
                self.happiness_change[frozenset(guest_pair)]
                for guest_pair in itertools.pairwise(guest_order))
            arrangement += self.happiness_change[frozenset([head, guest_order[0]])]
            arrangement += self.happiness_change[frozenset([head, guest_order[-1]])]
            if arrangement > best_arrangement:
                best_arrangement = arrangement
                log.log(log.INFO, f'New best order found {arrangement}: {head},{",".join(guest_order)}')

        return best_arrangement
