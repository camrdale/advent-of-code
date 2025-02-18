import aoc.input
from aoc import log
from aoc import runner

from year2019.day17 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        ascii = shared.AsciiProgram(intcode_input)
        log.log(log.INFO, ascii.map.print_map(additional_features={
            shared.DIRECTIONS[ascii.map.starting_direction]: set([ascii.map.starting_location])}))

        intersections = ascii.map.intersections()
        log.log(log.INFO, ascii.map.print_map(additional_features={
            'O': intersections,
            shared.DIRECTIONS[ascii.map.starting_direction]: set([ascii.map.starting_location])}))

        sum_alignment_parameters = sum(location.x*location.y for location in intersections)
        log.log(log.RESULT, f'The sum of the alignment parameters: {sum_alignment_parameters}')
        return sum_alignment_parameters


part = Part1()

part.add_result(5056)
