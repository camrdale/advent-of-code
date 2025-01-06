import math

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        time = int(''.join(input[0].split()[1:]))
        distance = int(''.join(input[1].split()[1:]))

        start = (time - math.sqrt(time**2 - (4 * distance))) / 2.0
        end = (time + math.sqrt(time**2 - (4 * distance))) / 2.0
        num_ways = math.ceil(end) - math.floor(start) - 1
        log(INFO, f'To win, hold for at least {start} and no more than {end}, which is {num_ways} ways')

        log(RESULT, f'The number of ways to win the race: {num_ways}')
        return num_ways


part = Part2()

part.add_result(71503, """
Time:      7  15   30
Distance:  9  40  200
""")

part.add_result(36872656)
