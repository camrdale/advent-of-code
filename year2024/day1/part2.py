from collections import defaultdict

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        left_input: list[int] = []
        right_input: dict[int, int] = defaultdict(int)
        for line in input:
            val = line.split()
            left_input.append(int(val[0]))
            right_input[int(val[1])] += 1

        similarity_score = 0
        for left in left_input:
            similarity_score += left * right_input[left]

        log(RESULT, 'Similarity Score:', similarity_score)
        return similarity_score


part = Part2()

part.add_result(31, """
3   4
4   3
2   5
1   3
3   9
3   3
""")

part.add_result(23177084)
