from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day12.shared import Plants


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        initial_state_input, spread_input = parser.get_two_part_input()

        plants = Plants(initial_state_input[0].split(': ')[1], spread_input)

        plants.advance_to(50_000_000_000)

        sum_indices = plants.sum_plant_indices()

        log.log(log.RESULT, f'After 50 billion generations the sum of the pots that contain plants: {sum_indices}')
        return sum_indices


part = Part2()

part.add_result(1000000000508)
