from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day17.shared import VaultRooms


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        rooms = VaultRooms(input[0])

        path = rooms.path()

        log.log(log.RESULT, f'The shortest path to the vault is length {path.length}: {path.previous}')
        return path.previous


part = Part1()

part.add_result('DDRRRD', """
ihgpwlah
""")

part.add_result('DDUDRLRRUDRD', """
kglvqrro
""")

part.add_result('DRURDRUDDLLDLUURRDULRLDUUDDDRR', """
ulqzkmiv
""")

part.add_result('RRRLDRDUDD', """
qtetzkpl
""")
