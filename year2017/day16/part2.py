import string

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day16.shared import dance


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        num_programs = int(parser.get_additional_params()[0])
        num_dances = int(parser.get_additional_params()[1])

        program_order = string.ascii_lowercase[:num_programs]
        dance_num = 0
        while dance_num < num_dances:
            program_order = dance(program_order, input[0])
            dance_num += 1
            if program_order == string.ascii_lowercase[:num_programs]:
                dance_num = (num_dances // dance_num) * dance_num
            log.log(log.INFO, f'After {dance_num:,} dances: {program_order}')

        log.log(log.RESULT, f'The order of the programs after their {num_dances:,} dances: {program_order}')
        return program_order


part = Part2()

part.add_result('abcde', """
s1
""", 5, 5)

part.add_result('ceadb', """
s1,x3/4,pe/b
""", 5, 2)

part.add_result('ceadb', """
s1,x3/4,pe/b
""", 5, 10)

part.add_result('cbolhmkgfpenidaj', None, 16, 1_000_000_000)
