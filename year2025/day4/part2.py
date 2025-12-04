import numpy
import scipy.ndimage

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        rolls_input = numpy.array([list(line) for line in input])
        rolls = numpy.zeros(rolls_input.shape, dtype=numpy.bool)
        rolls[rolls_input == '@'] = True

        total_removed = 0
        while True:
            adjacent = scipy.ndimage.convolve(
                rolls, [[1,1,1],[1,0,1],[1,1,1]], output=numpy.uint32, mode='constant', cval=0)
            accessible_rolls = rolls & (adjacent < 4)
            removed = accessible_rolls.sum()
            if removed == 0:
                break
            total_removed += removed
            rolls[accessible_rolls] = False

        log.log(log.RESULT, f'The total number of rolls removed: {total_removed}')
        return total_removed


part = Part2()

part.add_result(43, """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""")

part.add_result(8707)
