from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.chronal import OPERATIONS
from year2018.day16.shared import Sample


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        num_triples = 0
        for sample in Sample.from_input(parser):
            if len(sample.test_operations(OPERATIONS.values())) >= 3:
                num_triples += 1

        log.log(log.RESULT, f'The number of samples that behave like 3 or more opcodes: {num_triples}')
        return num_triples


part = Part1()

part.add_result(1, """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
""")

part.add_result(580)
