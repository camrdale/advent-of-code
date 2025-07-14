from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day14.shared import QuintupleHasher


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        hasher = QuintupleHasher(parser.get_input()[0], stretch_count=2016)

        keys = hasher.keys()

        key_64 = sorted(keys)[63]
        log.log(log.RESULT, f'64th key is found at index: {key_64}')
        return key_64


part = Part2()

part.add_result(22551, """
abc
""")

part.add_result(22045, """
yjdafjpo
""")
