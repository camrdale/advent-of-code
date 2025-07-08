from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day8.shared import parse_instructions


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        display = parse_instructions(input)
        
        num_lit = display.sum()
            
        log.log(log.RESULT, f'The number of lit pixels: "{num_lit}"')
        return num_lit


part = Part1()

part.add_result(119)
