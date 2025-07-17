from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day17.shared import VaultRooms


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        rooms = VaultRooms(input[0])

        path = rooms.path(short=False)

        log.log(log.RESULT, f'The longest path to the vault is length {path.length}: {path.previous}')
        return path.length


part = Part2()

part.add_result(370, """
ihgpwlah
""")

part.add_result(492, """
kglvqrro
""")

part.add_result(830, """
ulqzkmiv
""")

part.add_result(706, """
qtetzkpl
""")
