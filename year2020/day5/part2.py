from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day5.shared import from_binary_space


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        seat_ids = {from_binary_space(line) for line in input}

        missing_seats = set(range(min(seat_ids), max(seat_ids) + 1)) - seat_ids
        assert len(missing_seats) == 1, missing_seats

        seat_id = next(iter(missing_seats))
        log.log(log.RESULT, f'The missing seat ID: {seat_id}')
        return seat_id


part = Part2()

part.add_result(741)
