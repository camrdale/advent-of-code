from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day12.shared import Plants


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        initial_state_input, spread_input = parser.get_two_part_input()

        plants = Plants(initial_state_input[0].split(': ')[1], spread_input)

        plants.advance_to(20)
        
        sum_indices = plants.sum_plant_indices()

        log.log(log.RESULT, f'After 20 generations the sum of the pots that contain plants: {sum_indices}')
        return sum_indices


part = Part1()

part.add_result(325, """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""")

part.add_result(1733)
