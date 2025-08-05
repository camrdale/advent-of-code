from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        offsets = list(map(int, input))

        num_jumps = 0
        i = 0
        limit = len(offsets)
        while i < limit:
            offset = offsets[i]
            offsets[i] += 1 if offset < 3 else -1
            i += offset
            num_jumps += 1

        log.log(log.RESULT, f'The number of jumps to reach the exit: {num_jumps}')
        return num_jumps


part = Part2()

part.add_result(10, """
0
3
0
1
-3
""")

part.add_result(22570529)
