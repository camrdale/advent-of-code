from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day15.shared import Disc


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        discs: list[Disc] = []
        for line in input:
            discs.append(Disc.from_text(line))

        t = Disc.button_time(discs)

        log.log(log.RESULT, f'The first time you can press the button: {t}')
        return t


part = Part1()

part.add_result(5, """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
""")

part.add_result(203660)
