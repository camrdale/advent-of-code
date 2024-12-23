from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

from .shared import Towels


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        towel_input, design_input = parser.get_two_part_input()
        assert len(towel_input) == 1

        towels = Towels(towel_input[0])

        log(DEBUG, f'There are {len(towels.towels)} towels with max length {towels.max_length}')

        num_possible = 0
        for design in design_input:
            if len(design.strip()) == 0:
                continue

            possible = towels.build_design(design.strip())
            log(INFO, 'possible' if possible else 'NOT POSSIBLE', 'for design', design.strip())
            if possible:
                num_possible += 1

        log(RESULT, f'Number of possible designs: {num_possible}')
        return num_possible


part = Part1()

part.add_result(6, """
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

part.add_result(251)
