import functools

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


@functools.cache
def num_stones(value: int, blinks_remaining: int) -> int:
    if blinks_remaining == 0:
        return 1
    if value == 0:
        return num_stones(1, blinks_remaining - 1)
    s = str(value)
    if len(s) % 2 != 0:
        return num_stones(value * 2024, blinks_remaining - 1)
    n = len(s) // 2
    return num_stones(int(s[n:]), blinks_remaining - 1) + num_stones(int(s[:n]), blinks_remaining - 1)


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = list(map(int, parser.get_input()[0].split()))

        total_stones = 0
        for value in input:
            total_stones += num_stones(value, 75)

        log(RESULT, 'After 75 blinks the number of stones is:', total_stones)
        return total_stones


part = Part2()

part.add_result(65601038650482, """
125 17
""")

part.add_result(221683913164898)
