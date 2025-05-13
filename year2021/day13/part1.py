from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2021.day13.shared import fold


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        dot_input, fold_input = parser.get_two_part_input()

        dots: set[Coordinate] = set()
        for coords_input in dot_input:
            dots.add(Coordinate(*map(int, coords_input.split(','))))
        
        dots = fold(dots, fold_input[0])

        log.log(log.RESULT, 'Number of dots after one fold:', len(dots))
        return len(dots)


part = Part1()

part.add_result(17, """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""")

part.add_result(610)
