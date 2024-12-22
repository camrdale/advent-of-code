from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.runner import Part

from .shared import Garden


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        garden = Garden(input)

        log(DEBUG, garden)
        
        garden.merge()

        log(DEBUG, garden)

        total_price = garden.price()
        log(RESULT, 'Total garden price:', total_price)
        return total_price


part = Part1()

part.add_result(140, """
AAAA
BBCD
BBCC
EEEC
""")

part.add_result(772, """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""")

part.add_result(1930, """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""")

part.add_result(1361494)
