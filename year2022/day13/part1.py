from typing import Any

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day13.shared import compare_lists


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        sum_of_right_order_indices = 0
        for i, lines in enumerate(input):
            left: list[Any] = eval(lines[0])
            right: list[Any] = eval(lines[1])
            order = compare_lists(left, right)
            if order == 0:
                raise ValueError(f'Failed to determine if the order is correct for:\n  {left}\n  {right}')
            if order == -1:
                sum_of_right_order_indices += i+1
        
        log.log(log.RESULT, f'The sum of the indices of pairs that are in the right order: {sum_of_right_order_indices}')
        return sum_of_right_order_indices


part = Part1()

part.add_result(13, r"""
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""")

part.add_result(5252)
