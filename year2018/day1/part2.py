from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        frequency = 0
        frequencies: set[int] = set([frequency])
        while True:
            for delta in map(int, input):
                frequency += delta
                if frequency in frequencies:
                    log.log(log.RESULT, f'The first frequency reached twice: {frequency}')
                    return frequency
                frequencies.add(frequency)


part = Part2()

part.add_result(0, """
+1
-1
""")

part.add_result(10, """
+3
+3
+4
-2
-4
""")

part.add_result(5, """
-6
+3
+8
+5
-6
""")

part.add_result(14, """
+7
+7
-2
-7
-4
""")

part.add_result(73364)
