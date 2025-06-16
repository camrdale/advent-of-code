import operator
import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


SUE = re.compile(r'Sue ([0-9]*): (children|cats|samoyeds|pomeranians|akitas|vizslas|goldfish|trees|cars|perfumes): ([0-9]*), (children|cats|samoyeds|pomeranians|akitas|vizslas|goldfish|trees|cars|perfumes): ([0-9]*), (children|cats|samoyeds|pomeranians|akitas|vizslas|goldfish|trees|cars|perfumes): ([0-9]*)')
TARGET_TRAITS = {
    'children': (3, operator.eq),
    'cats': (7, operator.gt),
    'samoyeds': (2, operator.eq),
    'pomeranians': (3, operator.lt),
    'akitas': (0, operator.eq),
    'vizslas': (0, operator.eq),
    'goldfish': (5, operator.lt),
    'trees': (3, operator.gt),
    'cars': (2, operator.eq),
    'perfumes': (1, operator.eq),
}


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        matching_sue = 0
        for line in input:
            sue = SUE.match(line)
            assert sue is not None

            if not TARGET_TRAITS[sue.group(2)][1](int(sue.group(3)), TARGET_TRAITS[sue.group(2)][0]):
                continue
            if not TARGET_TRAITS[sue.group(4)][1](int(sue.group(5)), TARGET_TRAITS[sue.group(4)][0]):
                continue
            if not TARGET_TRAITS[sue.group(6)][1](int(sue.group(7)), TARGET_TRAITS[sue.group(6)][0]):
                continue

            assert matching_sue == 0, line
            matching_sue = int(sue.group(1))
            log.log(log.INFO, f'Found a match with Sue {matching_sue}: {line}')

        log.log(log.RESULT, f'The Sue that got the gift: {matching_sue}')
        return matching_sue


part = Part2()

part.add_result(405)
