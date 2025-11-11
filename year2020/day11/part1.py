import numpy
import scipy.ndimage

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Seats:
    def __init__(self, lines: list[str]) -> None:
        layout_input = numpy.array([list(line) for line in lines])
        self.layout = numpy.zeros(layout_input.shape, dtype=numpy.bool)
        self.layout[layout_input == 'L'] = True
        self.occupied = numpy.zeros(self.layout.shape, dtype=numpy.bool)

    def iterate_once(self) -> None:
        new_occupied = self.occupied.copy()

        adjacent = scipy.ndimage.convolve(
            self.occupied, [[1,1,1],[1,0,1],[1,1,1]], output=numpy.uint32, mode='constant', cval=0)
        new_occupied[self.layout & ~self.occupied & (adjacent == 0)] = True
        new_occupied[self.occupied & (adjacent >= 4)] = False

        self.occupied = new_occupied

    def iterate_until_stable(self) -> int:
        iterations = 0
        old_hash = self.hash()
        while True:
            self.iterate_once()
            iterations += 1
            hash = self.hash()
            if hash == old_hash:
                break
            old_hash = hash
        return iterations

    def hash(self) -> int:
        return hash(self.occupied.tobytes())

    def print(self) -> str:
        output = numpy.empty(self.layout.shape, dtype=numpy.str_)
        output[self.layout] = 'L'
        output[~self.layout] = '.'
        output[self.occupied] = '#'
        return '\n'.join(numpy.apply_along_axis(lambda row: ''.join(row), 1, output)) + '\n'

    def num_occupied(self) -> int:
        return self.occupied.sum()


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        seats = Seats(input)

        iterations = seats.iterate_until_stable()

        log.log(log.INFO, seats.print)

        num_occupied = seats.num_occupied()
        log.log(log.RESULT, f'After {iterations} rounds the chaos stabilizes with {num_occupied} occupied seats')
        return num_occupied


part = Part1()

part.add_result(37, """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""")

part.add_result(2152)
