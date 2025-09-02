from collections import Counter
import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        num_letters = Counter(itertools.chain.from_iterable([
            set(Counter(box_id).values())
            for box_id in input
        ]))

        checksum = num_letters[2] * num_letters[3]
        log.log(log.RESULT, f'The checksum for the list of box IDs is {num_letters[2]} x {num_letters[3]}: {checksum}')
        return checksum


part = Part1()

part.add_result(12, """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
""")

part.add_result(6972)
