import math

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day16.shared import Field


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        fields: list[Field] = [Field(line) for line in input[0]]

        tickets: list[list[int]] = [list(map(int, input[1][1].split(',')))]
        for ticket_input in input[2][1:]:
            ticket = list(map(int, ticket_input.split(',')))
            if all(Field.valid_for_any(value, fields) for value in ticket):
                tickets.append(ticket)

        num_fields = len(tickets[0])
        assert num_fields == len(fields)
        
        valid_fields: list[list[str]] = []
        for i in range(num_fields):
            valid_field: list[str] = []
            for field in fields:
                if all(field.valid(ticket[i]) for ticket in tickets):
                    valid_field.append(field.name)
            valid_fields.append(valid_field)
        
        field_names: list[str] = [''] * num_fields
        num_assigned = 0
        while num_assigned < num_fields:
            assigned = False
            for i, valid_field in enumerate(valid_fields):
                if len(valid_field) == 1:
                    field_names[i] = valid_field[0]
                    for valid_field in valid_fields:
                        if field_names[i] in valid_field:
                            valid_field.remove(field_names[i])
                    num_assigned += 1
                    assigned = True
                    break
            if not assigned:
                raise ValueError(f'Failed to assign any field: {valid_fields}')

        departure_product = math.prod([
            tickets[0][i]
            for i, field_name in enumerate(field_names)
            if field_name.startswith('departure')
        ])

        log.log(log.RESULT, f'The product of the departure fields: {departure_product}')
        return departure_product


part = Part2()

part.add_result(11, """
class: 0-1 or 4-19
departure row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""")

part.add_result(514662805187)
