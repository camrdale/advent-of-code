from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day15.shared import memory_game


N = 2020


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        last_number = memory_game(list(map(int, input[0].split(','))), N)

        log.log(log.RESULT, f'The {N}th number is: {last_number}')
        return last_number


part = Part1()

part.add_result(436, """
0,3,6
""")

part.add_result(1, """
1,3,2
""")

part.add_result(10, """
2,1,3
""")

part.add_result(27, """
1,2,3
""")

part.add_result(78, """
2,3,1
""")

part.add_result(438, """
3,2,1
""")

part.add_result(1836, """
3,1,2
""")

part.add_result(240, """
14,8,16,0,1,17
""")
