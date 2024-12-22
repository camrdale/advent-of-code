from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.runner import Part

from .shared import Garden


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        garden = Garden(input)

        log(DEBUG, garden)
        
        garden.merge()

        log(DEBUG, garden)

        discounted_price = garden.discounted_price()
        log(RESULT, 'Discounted total garden price:', discounted_price)
        return discounted_price


part = Part2()

part.add_result(80, """
AAAA
BBCD
BBCC
EEEC
""")

part.add_result(436, """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""")

part.add_result(236, """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""")

part.add_result(368, """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""")

part.add_result(1206, """
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

part.add_result(830516)
