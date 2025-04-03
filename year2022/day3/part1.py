from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day3.shared import Rucksack


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_priorities = 0
        for line in input:
            rucksack = Rucksack.from_text(line)
            in_both = rucksack.in_both_compartments()
            log.log(log.INFO, f'Rucksack contains {rucksack.first_compartment()} and {rucksack.second_compartment()}, with {in_both} in both, a priority of {in_both.priority()}')
            total_priorities += in_both.priority()
        
        log.log(log.RESULT, f'The sum of the priorities of the missplaced items: {total_priorities}')
        return total_priorities


part = Part1()

part.add_result(157, r"""
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""")

part.add_result(8088)
