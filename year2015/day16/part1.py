import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


SUE = re.compile(r'Sue ([0-9]*): (children|cats|samoyeds|pomeranians|akitas|vizslas|goldfish|trees|cars|perfumes): ([0-9]*), (children|cats|samoyeds|pomeranians|akitas|vizslas|goldfish|trees|cars|perfumes): ([0-9]*), (children|cats|samoyeds|pomeranians|akitas|vizslas|goldfish|trees|cars|perfumes): ([0-9]*)')
TARGET_TRAITS = set([
    ('children', 3),
    ('cats', 7),
    ('samoyeds', 2),
    ('pomeranians', 3),
    ('akitas', 0),
    ('vizslas', 0),
    ('goldfish', 5),
    ('trees', 3),
    ('cars', 2),
    ('perfumes', 1),
])


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        matching_sue = 0
        for line in input:
            sue = SUE.match(line)
            assert sue is not None

            sue_traits = set([
                (sue.group(2), int(sue.group(3))),
                (sue.group(4), int(sue.group(5))),
                (sue.group(6), int(sue.group(7))),
            ])

            if sue_traits <= TARGET_TRAITS:
                assert matching_sue == 0, line
                matching_sue = int(sue.group(1))
                log.log(log.INFO, f'Found a match with Sue {matching_sue}: {line}')

        log.log(log.RESULT, f'The Sue that got the gift: {matching_sue}')
        return matching_sue


part = Part1()

part.add_result(103)
