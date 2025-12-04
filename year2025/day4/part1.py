import numpy
import scipy.ndimage

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        rolls_input = numpy.array([list(line) for line in input])
        rolls = numpy.zeros(rolls_input.shape, dtype=numpy.bool)
        rolls[rolls_input == '@'] = True
        adjacent = scipy.ndimage.convolve(
            rolls, [[1,1,1],[1,0,1],[1,1,1]], output=numpy.uint32, mode='constant', cval=0)
        accessible_rolls = (rolls & (adjacent < 4)).sum()

        log.log(log.RESULT, f'The number of accessible rolls: {accessible_rolls}')
        return accessible_rolls


part = Part1()

part.add_result(13, """
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

part.add_result(1537)
