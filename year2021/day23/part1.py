from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day23.shared import BurrowMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        estimated_iterations, progress_desc_suffix = parser.get_additional_params()

        burrow = BurrowMap(input)

        with log.ProgressBar(estimated_iterations=estimated_iterations, desc=f'day 23,1,{progress_desc_suffix}') as progress_bar:
            energy = burrow.organize(progress_bar)

        log.log(log.RESULT, f'The least energy required to organize the amphipods: {energy}')
        return energy


part = Part1()

part.add_result(12521, """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""", 20150, 'test1', include_progress=True)

part.add_result(16244, None, 91000, 'final')
