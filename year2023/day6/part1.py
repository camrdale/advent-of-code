import math

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        times = list(map(int, input[0].split()[1:]))
        distances = list(map(int, input[1].split()[1:]))

        product_num_ways = 1
        for time, distance in zip(times, distances):
            start = (time - math.sqrt(time**2 - (4 * distance))) / 2.0
            end = (time + math.sqrt(time**2 - (4 * distance))) / 2.0
            num_ways = (math.ceil(end) - 1) - (math.floor(start) + 1) + 1
            log(INFO, f'To win, hold for at least {start} and no more than {end}, which is {num_ways} ways')
            product_num_ways *= num_ways

        log(RESULT, f'The product of the number of ways to win each race: {product_num_ways}')
        return product_num_ways


part = Part1()

part.add_result(288, """
Time:      7  15   30
Distance:  9  40  200
""")

part.add_result(393120)
