from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day8.shared import Node


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        license_file = list(map(int, input[0].split()))

        root, length = Node.parse(license_file, 0)
        assert length == len(license_file)

        root_value = root.value()

        log.log(log.RESULT, f'The value of the root node: {root_value}')
        return root_value


part = Part2()

part.add_result(66, """
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
""")

part.add_result(24453)
