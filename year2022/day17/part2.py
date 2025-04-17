from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day17.shared import TetrisMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        tetris_map = TetrisMap(parser.get_input()[0])

        height = tetris_map.simulate_by_repetition(1000000000000)

        log.log(log.RESULT, f'After 1000000000000 rocks have fallen, the height of the tower is: {height}')
        return height


part = Part2()

# part.add_result(1514285714288, r"""
# >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
# """)

part.add_result(1514369501484)
