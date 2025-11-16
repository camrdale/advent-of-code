from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day16.shared import Field


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        fields: list[Field] = [Field(line) for line in input[0]]
        
        scanning_error_rate = 0
        for ticket_input in input[2][1:]:
            ticket = list(map(int, ticket_input.split(',')))
            for value in ticket:
                if not Field.valid_for_any(value, fields):
                    scanning_error_rate += value

        log.log(log.RESULT, f'The ticket scanning error rate is: {scanning_error_rate}')
        return scanning_error_rate


part = Part1()

part.add_result(71, """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""")

part.add_result(32835)
