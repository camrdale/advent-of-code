from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        points = 0
        for line in input:
            _, number_input = line.split(':')
            winning_input, my_input = number_input.strip().split('|')
            winning_numbers = set(winning_input.strip().split())
            my_numbers = set(my_input.strip().split())
            num_winning = len(winning_numbers.intersection(my_numbers))
            if num_winning > 0:
                points += 2**(num_winning - 1)

        log(RESULT, f'The total points from all cards: {points}')
        return points


part = Part1()

part.add_result(13, """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""")

part.add_result(17782)
