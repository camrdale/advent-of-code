from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day24.shared import Monad, Equality


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        monad = Monad(input)

        equalities = Equality.parseProgram(input)

        model_number = [9]*14
        for equality in equalities:
            pushed_digit_value = min(equality.range_for_pushed_digit())
            model_number[equality.pushed_value.digit] = pushed_digit_value
            model_number[equality.digit] = equality.digit_value(pushed_digit_value)

        z = monad.validate(list(model_number))
        assert z == 0, f'{"".join(map(str, model_number))} -> {z}'

        log.log(log.RESULT, f'The smallest model number accepted by MONAD: {"".join(map(str, model_number))}')
        return int("".join(map(str, model_number)))


part = Part2()

part.add_result(61191516111321)

# 61191516117921
# 61191516111321
