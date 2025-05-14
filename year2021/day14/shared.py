from collections import Counter
import itertools

import cachetools

from aoc import log


MAX_CACHE_SIZE = 20000000


class PolymerConstructor:
    def __init__(self, pair_insertion_rules_input: list[str]) -> None:
        self.pair_insertion_rules: dict[str, str] = {}
        for line in pair_insertion_rules_input:
            pair, insertion = line.split(' -> ')
            self.pair_insertion_rules[pair] = insertion
        self.cache: cachetools.LRUCache[tuple[str], int] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)

    @cachetools.cachedmethod(lambda self: self.cache)
    def _count_letters(self, polymer_pair: str, remaining_steps: int) -> Counter[str]:
        if remaining_steps == 0:
            return Counter(polymer_pair)
        insert = self.pair_insertion_rules[polymer_pair]
        return (
            self._count_letters(polymer_pair[0] + insert, remaining_steps - 1)
            + self._count_letters(insert + polymer_pair[1], remaining_steps - 1)
            # Remove one of the inserted letter which is counted twice in the calls above.
            - Counter({insert: 1}))

    def most_minus_least_letters(self, polymer_template: str, steps: int) -> int:
        # Include the first letter, as it is not counted twice.
        total_counter = Counter(polymer_template[0])
        for polymer_pair in itertools.pairwise(polymer_template):
            total_counter.update(
                self._count_letters(polymer_pair[0] + polymer_pair[1], steps)
                # Remove the first letter in the pair as it will be counted twice.
                - Counter({polymer_pair[0]: 1}))
        most_common = total_counter.most_common()
        log.log(log.INFO, most_common)
        return most_common[0][1] - most_common[-1][1]
