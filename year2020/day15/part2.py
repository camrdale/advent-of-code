from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day15.shared import memory_game


N = 30_000_000


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        last_number = memory_game(list(map(int, input[0].split(','))), N)

        log.log(log.RESULT, f'The {N}th number is: {last_number}')
        return last_number


part = Part2()

part.add_result(175594, """
0,3,6
""")

# Examples are too slow.
# part.add_result(2578, """
# 1,3,2
# """)

# part.add_result(3544142, """
# 2,1,3
# """)

# part.add_result(261214, """
# 1,2,3
# """)

# part.add_result(6895259, """
# 2,3,1
# """)

# part.add_result(18, """
# 3,2,1
# """)

# part.add_result(362, """
# 3,1,2
# """)

part.add_result(505, """
14,8,16,0,1,17
""")
