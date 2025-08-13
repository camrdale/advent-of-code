from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        depths = list(map(int, [line.split(': ')[0] for line in input]))
        ranges = list(map(int, [line.split(': ')[1] for line in input]))
        periods = [(n - 1) * 2 for n in ranges]

        delay = 0
        while True:
            delay += 1
            for depth, period in zip(depths, periods):
                if (depth + delay) % period == 0:
                    break
            else:
                log.log(log.RESULT, f'The shortest delay to not get caught: {delay}')
                return delay


part = Part2()

part.add_result(10, """
0: 3
1: 2
4: 4
6: 4
""")

part.add_result(3896406)
