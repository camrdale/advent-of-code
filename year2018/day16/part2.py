from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day16.shared import Sample, Operation, OPERATIONS


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        # Opcode and their known operation
        operations: dict[int, type[Operation]] = {}

        # Unknown opcodes and which operations they could possibly be.
        unknown_operations: dict[int, list[type[Operation]]] = {i: list(OPERATIONS) for i in range(16)}

        # Limit the possibilities based on the samples.
        for sample in Sample.from_input(parser):
            unknown_operations[sample.opcode()] = sample.test_operations(unknown_operations[sample.opcode()])

        while unknown_operations:
            # Find an opcode that only has a single possible operation remaining.
            num_ops, opcode, ops = min(
                (len(ops), opcode, ops) for opcode, ops in unknown_operations.items())
            assert num_ops == 1, unknown_operations

            # Assign the operation to the opcode.
            known_operation = ops[0]
            del unknown_operations[opcode]
            operations[opcode] = known_operation
            log.log(log.INFO, f'{opcode} must be {known_operation}')

            # Remove the known operation from the other possibilities.
            for ops in unknown_operations.values():
                if known_operation in ops:
                    ops.remove(known_operation)

        assert len(unknown_operations) == 0, unknown_operations

        instructions: list[Operation] = []
        for instruction_input in parser.get_multipart_input()[-1]:
            opcode, a, b, c = map(int, instruction_input.split())
            instructions.append(operations[opcode](a, b, c))

        registers = {i: 0 for i in range(4)}
        for instruction in instructions:
            instruction.apply(registers)

        log.log(log.RESULT, f'The registers after running the test program: {registers}')
        return registers[0]


part = Part2()

part.add_result(537)
