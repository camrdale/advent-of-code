from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

import operator
from collections.abc import Callable


OPS: dict[str, Callable[[int, int], int]] = {
    '+': operator.add,
    '*': operator.mul,
}


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        all_values = [map(int, line.split()) for line in input[:-1]]
        ops: map[Callable[[int, int], int]] = map(OPS.__getitem__, input[-1].split())

        total = 0
        for op, *values in zip(ops, *all_values):
            val = values[0]
            for next_val in values[1:]:
                val = op(val, next_val)
            total += val

        log.log(log.RESULT, f'The total of all the problems: {total}')
        return total


part = Part1()

part.add_result(4277556, """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""")

part.add_result(7098065460541)
