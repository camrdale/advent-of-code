import string

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day16.shared import dance


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        num_programs = int(parser.get_additional_params()[0])

        program_order = dance(string.ascii_lowercase[:num_programs], input[0])

        log.log(log.RESULT, f'The order of the programs after their dance: {program_order}')
        return program_order


part = Part1()

part.add_result('baedc', """
s1,x3/4,pe/b
""", 5)

part.add_result('cknmidebghlajpfo', None, 16)
