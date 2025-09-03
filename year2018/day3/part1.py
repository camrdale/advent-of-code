from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day3.shared import Claim


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        claims: list[Claim] = []
        for line in input:
            claims.append(Claim.from_text(line))

        fabric = Claim.sum(claims)

        overlaps = (fabric > 1).sum()

        log.log(log.RESULT, f'The square inches of fabric in 2 or more claims: {overlaps}')
        return overlaps


part = Part1()

part.add_result(4, """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""")

part.add_result(109716)
