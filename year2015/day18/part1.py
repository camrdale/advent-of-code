from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day18.shared import LightGrid


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        steps = int(parser.get_additional_params()[0])

        lights = LightGrid(input)

        for _ in range(steps):
            lights.step()

        num_on = lights.num_on()

        log.log(log.RESULT, f'After {steps} steps, the number of on lights: {num_on}')
        return num_on


part = Part1()

part.add_result(4, """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""", 4)

part.add_result(1061, None, 100)
