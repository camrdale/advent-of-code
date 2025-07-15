from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day15.shared import Disc


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        discs: list[Disc] = []
        for line in input:
            discs.append(Disc.from_text(line))

        discs.append(Disc(discs[-1].num + 1, 11, 0))

        t = Disc.button_time(discs)

        log.log(log.RESULT, f'The first time you can press the button: {t}')
        return t


part = Part2()

part.add_result(2408135)
