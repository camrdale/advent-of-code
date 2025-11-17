from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day17.shared import PocketDimension, NUM_ITER


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        dimension = PocketDimension(input, 4)

        for _ in range(NUM_ITER):
            dimension.iterate_once()
        
        num_active = dimension.num_occupied()
        log.log(log.RESULT, f'The number of active cubes after {NUM_ITER} iterations: {num_active}')
        return num_active


part = Part2()

part.add_result(848, """
.#.
..#
###
""")

part.add_result(2056)
