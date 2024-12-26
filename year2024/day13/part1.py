from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import parse, win


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        machines = parse(parser)

        total_tokens = 0
        wins = 0
        for machine in machines:
            tokens = win(machine)
            if tokens is not None:
                total_tokens += tokens
                wins += 1

        log(RESULT, 'Total tokens to win', wins, 'prizes:', total_tokens)
        return total_tokens


part = Part1()

part.add_result(480, """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""")

part.add_result(31589)
