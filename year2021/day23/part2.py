from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day23.shared import BurrowMap


UNFOLDED_LINES = [
    '  #D#C#B#A#',
    '  #D#B#A#C#'
    ]


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        estimated_iterations, progress_desc_suffix = parser.get_additional_params()

        input = input[:3] + UNFOLDED_LINES + input[3:]

        burrow = BurrowMap(input)

        with log.ProgressBar(estimated_iterations=estimated_iterations, desc=f'day 23,2,{progress_desc_suffix}') as progress_bar:
            energy = burrow.organize(progress_bar)

        log.log(log.RESULT, f'The least energy required to organize the amphipods: {energy}')
        return energy


part = Part2()

part.add_result(44169, """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""", 174000, 'test1', include_progress=True)

part.add_result(43226, None, 161000, 'final')
