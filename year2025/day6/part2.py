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

        start = 0
        total = 0
        while start < len(input[0]):
            end = start
            for i in range(len(input)):
                while end < len(input[i]) and input[i][end] != ' ':
                    end += 1

            op = OPS[input[-1][start:end].strip()]
            val = 0 if op == operator.add else 1

            for i in range(end - 1, start - 1, -1):
                next_val = int(''.join([line[i] for line in input[:-1]]))
                val = op(val, next_val)

            total += val
            start = end + 1

        log.log(log.RESULT, f'The total of all the problems: {total}')
        return total


part = Part1()

part.add_result(3263827, """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""")

part.add_result(13807151830618)
