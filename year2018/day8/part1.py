from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day8.shared import Node


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        license_file = list(map(int, input[0].split()))

        root, length = Node.parse(license_file, 0)
        assert length == len(license_file)

        metadata_sum = root.sum_metadata()

        log.log(log.RESULT, f'The sum of all the metadata entries: {metadata_sum}')
        return metadata_sum


part = Part1()

part.add_result(138, """
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
""")

part.add_result(38567)
