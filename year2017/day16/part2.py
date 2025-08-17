import string

import numpy
import numpy.typing

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day16.shared import dance


def dance_matrices(num_programs: int, moves: str) -> tuple[numpy.typing.NDArray[numpy.uint8], numpy.typing.NDArray[numpy.uint8]]:
    """Create two matrices for permuting the program dance.
    
    The first matrix contains changes to the domain of the program list
    (partner swaps) and must be applied to the left of the program array.
    The second matrix contains changes to the positions of the programs
    (spins and exchanges) and must be applied to the right of the program
    array.
    """
    left = numpy.identity(num_programs, numpy.uint8)
    right = numpy.identity(num_programs, numpy.uint8)
    for move in moves.split(','):
        match move[0]:
            case 's':
                spin = int(move[1:])
                s = numpy.roll(numpy.identity(num_programs, numpy.uint8), spin, 1)
                right @= s
            case 'x':
                swap1, swap2 = map(int, move[1:].split('/'))
                x = numpy.identity(num_programs, numpy.uint8)
                x[[swap1, swap2]] = x[[swap2, swap1]]
                right @= x
            case 'p':
                swap1 = string.ascii_lowercase.index(move[1])
                swap2 = string.ascii_lowercase.index(move[3])
                p = numpy.identity(num_programs, numpy.uint8)
                p[[swap1, swap2]] = p[[swap2, swap1]]
                left @= p
            case _:
                raise ValueError(f'Failed to parse dance move: {move}')
    return left, right


# 90 ms
def with_matrices(input: list[str], num_programs: int, num_dances: int) -> str:
    left, right = dance_matrices(num_programs, input[0])

    start = numpy.array(range(num_programs), numpy.uint8)
    # Multiply the two permutation matrices by themselves the number of required dances times.
    left = numpy.linalg.matrix_power(left, num_dances)
    right = numpy.linalg.matrix_power(right, num_dances)

    return ''.join(string.ascii_lowercase[i] for i in left @ start @ right)


# 260 ms
def with_cycle_detection(input: list[str], num_programs: int, num_dances: int) -> str:
    program_order = string.ascii_lowercase[:num_programs]
    dance_num = 0
    while dance_num < num_dances:
        program_order = dance(program_order, input[0])
        dance_num += 1
        if program_order == string.ascii_lowercase[:num_programs]:
            dance_num = (num_dances // dance_num) * dance_num
        log.log(log.INFO, f'After {dance_num:,} dances: {program_order}')

    return program_order


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        num_programs = int(parser.get_additional_params()[0])
        num_dances = int(parser.get_additional_params()[1])

        program_order = with_matrices(input, num_programs, num_dances)

        log.log(log.RESULT, f'The order of the programs after their {num_dances:,} dances: {program_order}')
        return program_order


part = Part2()

part.add_result('abcde', """
s1
""", 5, 5)

part.add_result('ceadb', """
s1,x3/4,pe/b
""", 5, 2)

part.add_result('ceadb', """
s1,x3/4,pe/b
""", 5, 10)

part.add_result('cbolhmkgfpenidaj', None, 16, 1_000_000_000)
