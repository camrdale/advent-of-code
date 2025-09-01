from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        frequency = sum(map(int, input))

        log.log(log.RESULT, f'The resulting frequency: {frequency}')
        return frequency


part = Part1()

part.add_result(3, """
+1
-2
+3
+1
""")

part.add_result(522)
