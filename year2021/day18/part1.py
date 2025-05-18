from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day18.shared import Snailfish


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        snailfish_sum, length = Snailfish.parse_text(input[0])
        assert length == len(input[0])
        log.log(log.INFO, f'First number: {snailfish_sum}')
        for line in input[1:]:
            snailfish_num, length = Snailfish.parse_text(line)
            assert length == len(line)
            log.log(log.INFO, f'Adding number: {snailfish_num}')

            snailfish_sum = snailfish_sum.add(snailfish_num)
            log.log(log.INFO, f'Reduced new number: {snailfish_sum}')

        magnitude = snailfish_sum.magnitude()
        log.log(log.RESULT, 'The magnitude of the final sum:', magnitude)
        return magnitude


part = Part1()

part.add_result(143, """
[1,2]
[[3,4],5]
""")

part.add_result(1384, """
[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]
""")

part.add_result(445, """
[1,1]
[2,2]
[3,3]
[4,4]
""")

part.add_result(791, """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
""")

part.add_result(1137, """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
""")

part.add_result(3488, """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""")

part.add_result(4140, """
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

part.add_result(4243)
