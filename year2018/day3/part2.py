from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day3.shared import Claim


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        claims: list[Claim] = []
        for line in input:
            claims.append(Claim.from_text(line))

        fabric = Claim.sum(claims)

        for claim in claims:
            if (fabric[claim.area()] == 1).all():
                log.log(log.RESULT, f'The claim that has no overlaps: {claim}')
                return claim.id
            
        raise ValueError(f'Failed to find a claim with no overlaps')


part = Part2()

part.add_result(3, """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""")

part.add_result(124)
