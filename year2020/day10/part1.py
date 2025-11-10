from collections import Counter
import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        adapters = sorted(map(int, input))

        differences: Counter[int] = Counter([adapters[0], 3])

        for a, b in itertools.pairwise(adapters):
            differences[b - a] += 1

        log.log(log.RESULT, f'The differences are: {differences} ({differences[1] * differences[3]})')
        return differences[1] * differences[3]


part = Part1()

part.add_result(35, """
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

part.add_result(220, """
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

part.add_result(2592)
