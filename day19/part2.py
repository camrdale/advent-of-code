from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

from .shared import Towels


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        towels = Towels(input[0])

        log(DEBUG, f'There are {len(towels.towels)} towels with max length {towels.max_length}')

        num_possible = 0    
        for design in input[1:]:
            if len(design) == 0:
                continue

            possible = towels.build_design(design)
            log(INFO, f'possible {possible} ways' if possible > 0 else 'NOT POSSIBLE', 'for design', design)
            num_possible += possible

        log(RESULT, f'Number of possible designs: {num_possible}')
        return num_possible


part = Part2()

part.add_result(16, """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""")

part.add_result(616957151871345)
