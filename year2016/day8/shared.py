import re

import numpy
import numpy.typing


INSTRUCTION = re.compile(r'(rect |rotate row y=|rotate column x=)([0-9]*)(?:x| by )([0-9]*)')


def parse_instructions(instructions: list[str]) -> numpy.typing.NDArray[numpy.bool]:
    display = numpy.zeros((6, 50), dtype=numpy.bool)

    for line in instructions:
        instruction = INSTRUCTION.match(line)
        assert instruction, line

        match instruction.group(1):
            case 'rect ':
                columns = int(instruction.group(2))
                rows = int(instruction.group(3))
                display[:rows, :columns] = numpy.ones((rows, columns), dtype=numpy.bool)
            case 'rotate row y=':
                row = int(instruction.group(2))
                columns = int(instruction.group(3))
                display[row, :] = numpy.roll(display[row, :], columns)
            case 'rotate column x=':
                column = int(instruction.group(2))
                rows = int(instruction.group(3))
                display[:, column] = numpy.roll(display[:, column], rows)
            case _:
                raise ValueError(f'Unexpected')

    return display
