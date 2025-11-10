import functools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


@functools.cache
def num_arrangements(adapters: tuple[int], start: int, end: int) -> int:
    if not adapters:
        return 1 if end - start <= 3 else 0
    result = 0
    for i in range(len(adapters)):
        if adapters[i] <= start + 3:
            result += num_arrangements(adapters[i+1:], adapters[i], end)
    return result


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        adapters = sorted(map(int, input))

        arrangements = num_arrangements(tuple(adapters), 0, adapters[-1] + 3)

        log.log(log.RESULT, f'The differences are: {arrangements}')
        return arrangements


part = Part2()

part.add_result(8, """
16
10
15
5
1
11
7
19
6
12
4
""")

part.add_result(19208, """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
""")

part.add_result(198428693313536)
