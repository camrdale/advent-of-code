import math

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


def num_presents(house: int) -> int:
    step = 1
    if house % 2 == 1:
        step = 2

    presents = 0
    for elf in range(1, int(math.sqrt(house)) + 1, step):
        if house % elf == 0:
            presents += 10 * elf
            if elf != house // elf:
                presents += 10 * (house // elf)
    
    return presents


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        target_presents = int(input[0])

        lower_bound = int(math.sqrt(2 * target_presents / 10))
        upper_bound = target_presents // 10

        for house in log.progress_bar(range(lower_bound, upper_bound + 1), desc='day 20,1'):
            presents = num_presents(house)
            if presents >= target_presents:
                log.log(log.RESULT, f'{presents} presents are received by house number: {house}')
                return house
        
        raise ValueError(f'Failed to find a house in the range {lower_bound}-{upper_bound} that received at least {target_presents} presents')


part = Part1()

part.add_result(10, '160')

part.add_result(831600, '36000000')
