from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day17.shared import TetrisMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        tetris_map = TetrisMap(parser.get_input()[0])

        height = tetris_map.simulate(2022)

        log.log(log.DEBUG, tetris_map.print_map())

        log.log(log.RESULT, f'After 2022 rocks have fallen, the height of the tower is: {height}')
        return height


part = Part1()

part.add_result(3068, r"""
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""")

part.add_result(3067)
