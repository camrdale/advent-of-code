import itertools
from collections.abc import Generator

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day3.shared import Rucksack


def batched(iterable: list[str], n: int) -> Generator[tuple[str, ...], str, None]:
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        if len(batch) != n:
            raise ValueError('batched(): incomplete batch')
        yield batch


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_priorities = 0
        for first_elf, second_elf, third_elf in batched(input, 3):
            first_rucksack = Rucksack.from_text(first_elf)
            second_rucksack = Rucksack.from_text(second_elf)
            third_rucksack = Rucksack.from_text(third_elf)
            group_badge = first_rucksack.group_badge(second_rucksack, third_rucksack)
            log.log(log.INFO, f'Elves carrying {first_rucksack}, {second_rucksack} and {third_rucksack} have group badge {group_badge}, with a priority of {group_badge.priority()}')
            total_priorities += group_badge.priority()
        
        log.log(log.RESULT, f'The sum of the priorities of the group badges: {total_priorities}')
        return total_priorities


part = Part2()

part.add_result(70, r"""
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""")

part.add_result(2522)
