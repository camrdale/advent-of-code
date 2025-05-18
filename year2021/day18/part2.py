import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day18.shared import Snailfish


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        max_magnitude = 0
        for left, right in itertools.permutations(input, 2):
            snailfish_left, length = Snailfish.parse_text(left)
            assert length == len(left)

            snailfish_right, length = Snailfish.parse_text(right)
            assert length == len(right)

            snailfish_sum = snailfish_left.add(snailfish_right)

            magnitude = snailfish_sum.magnitude()
            if magnitude > max_magnitude:
                max_magnitude = magnitude
                max_left = snailfish_left
                max_right = snailfish_right
                max_sum = snailfish_sum

        log.log(log.INFO, f'Max is {max_left} + {max_right} = {max_sum}') # type: ignore
        log.log(log.RESULT, 'The magnitude of the final sum:', max_magnitude)
        return max_magnitude


part = Part2()

part.add_result(3993, """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""")

part.add_result(4701)
