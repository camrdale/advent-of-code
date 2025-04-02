from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day2.shared import HandShape


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_score = 0
        for line in input:
            opponent_str, response_str = line.split()
            opponent = HandShape(opponent_str)
            response = HandShape(response_str)
            total_score += response.round_score(opponent)
        
        log.log(log.RESULT, f'The total score from all rounds: {total_score}')
        return total_score


part = Part1()

part.add_result(15, r"""
A Y
B X
C Z
""")

part.add_result(12772)
