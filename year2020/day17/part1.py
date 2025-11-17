from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day17.shared import PocketDimension, NUM_ITER


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        dimension = PocketDimension(input, 3)

        for _ in range(NUM_ITER):
            log.log(log.DEBUG, dimension.print)
            dimension.iterate_once()
        
        log.log(log.INFO, dimension.print)
        num_active = dimension.num_occupied()
        log.log(log.RESULT, f'The number of active cubes after {NUM_ITER} iterations: {num_active}')
        return num_active


part = Part1()

part.add_result(112, """
.#.
..#
###
""")

part.add_result(310)
