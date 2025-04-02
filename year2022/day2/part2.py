from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day2.shared import HandShape


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_score = 0
        for line in input:
            opponent_str, result = line.split()
            opponent = HandShape(opponent_str)
            response = HandShape.for_result(opponent, result)
            total_score += response.round_score(opponent)
        
        log.log(log.RESULT, f'The total score from all rounds: {total_score}')
        return total_score


part = Part2()

part.add_result(12, r"""
A Y
B X
C Z
""")

part.add_result(11618)
