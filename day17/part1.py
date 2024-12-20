from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import parse


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        state, program = parse(parser.get_input())

        program.execute(state)

        result = ','.join(map(str, state.out))
        log(RESULT, 'Program output:', result)

        return result


part = Part1()

part.add_result('4,6,3,5,6,3,5,2,1,0', """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""")

part.add_result('5,1,3,4,3,7,2,1,7')
