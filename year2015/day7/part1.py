import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day7.shared import Operation


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        operations: dict[str, Operation] = collections.defaultdict(Operation)
        for line in input:
            instruction = Operation.parse_text(line)
            operation = operations[instruction.group(4)]
            operation.initialize(instruction, operations)

        a_value = operations['a'].value()
        log.log(log.RESULT, f'The signal provided to wire "a": {a_value}')
        return a_value


part = Part1()

part.add_result(16076)
