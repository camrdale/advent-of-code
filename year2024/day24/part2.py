from collections import defaultdict
import math
import random

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

from .shared import Operation, LogicEquation, to_num, calculate_z


def test_equations(equations: dict[str, LogicEquation], num_bits:int) -> bool:
    """Test the equations to see if they work for numbers with max num_bits."""
    # Runs over 30,000 tests for 45 bits, only a thousand for less than 30 bits.
    num_tests = math.ceil(2**(num_bits*15/45)) + 1000
    for _ in range(num_tests):
        x = random.randint(0, 2**num_bits - 1)
        y = random.randint(0, 2**num_bits - 1)
        format_string = '{0:0' + str(num_bits) + 'b}'
        known_bits: dict[str, int] = dict((f'x{i:02}', int(b)) for i, b in enumerate(reversed(format_string.format(x))))
        known_bits.update(dict((f'y{i:02}', int(b)) for i, b in enumerate(reversed(format_string.format(y)))))
        z = calculate_z(known_bits, equations, num_bits=num_bits)
        expected = (x + y) % 2**num_bits
        if z != expected:
            return False
    return True


def find_swap(
        swap_out: list[str],
        swap_in: list[str],
        initial_equations: dict[str, LogicEquation],
        num_bits:int
        ) -> tuple[str, str] | None:
    """Find a swap that causes the equations to work for numbers with max num_bits."""
    for result in swap_out:
        for possibility in swap_in:
            if result == possibility:
                continue
            # Don't create an infinite loop by having an equation depend on it's own result.
            if (possibility in initial_equations[result].depends_on_all(initial_equations)
                or result in initial_equations[possibility].depends_on_all(initial_equations)):
                continue

            log(DEBUG, f'    Trying candidate swap {result} <-> {possibility}')
            equations = dict(initial_equations)
            equations[result], equations[possibility] = equations[possibility], equations[result]
            if test_equations(equations, num_bits):
                log(DEBUG, f'      FOUND successful swap {result} <-> {possibility}')
                return result, possibility
    print(f'ERROR: failed to find a swap for {num_bits}: {swap_out} <-> {swap_in}')


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        bits_input, logic_input = parser.get_two_part_input()

        known_bits: dict[str, int] = {}
        for line in bits_input:
            bit, value = line.split(': ')
            known_bits[bit] = int(value)

        x = to_num('x', known_bits)
        y = to_num('y', known_bits)
        expected = x + y
        
        initial_equations: dict[str, LogicEquation] = {}
        for line in logic_input:
            lhs, operation, rhs, _, result = line.split()
            initial_equations[result] = LogicEquation.deterministic(lhs, Operation[operation], rhs)
        initial_equation_results: dict[LogicEquation, str] = dict(
            (equation, result) for result, equation in initial_equations.items())

        equation_max_bit: dict[str, int] = {}
        for result, equation in initial_equations.items():
            equation_max_bit[result] = equation.depends_on_max_bit(known_bits, initial_equations)

        z = calculate_z(dict(known_bits), initial_equations)
        log(INFO, f'Got:      {z:045b}')
        log(INFO, f'Expected: {expected:045b}')
        log(RESULT, 'Number of wrong bits', (z ^ expected).bit_count())

        swapped: list[str] = []
        known_good_equations: set[LogicEquation] = set()
        known_good_equations.update(initial_equations[f'z00'].depends_on_equations(initial_equations))
        known_good_equations.update(initial_equations[f'z01'].depends_on_equations(initial_equations))
        for z_bit in range(2, 45):
            z_equation = initial_equations[f'z{z_bit:02}']
            new_equations = z_equation.depends_on_equations(initial_equations) - known_good_equations

            # There seems to always be a z10 = x10 XOR y10
            expected_this_bit = LogicEquation(f'x{z_bit:02}', Operation.XOR, f'y{z_bit:02}')
            if expected_this_bit in new_equations:
                known_good_equations.add(expected_this_bit)
                new_equations.remove(expected_this_bit)
            # There also seems to always be a z10 = x09 AND y09
            expected_last_bit = LogicEquation(f'x{z_bit-1:02}', Operation.AND, f'y{z_bit-1:02}')
            if expected_last_bit in new_equations:
                known_good_equations.add(expected_last_bit)
                new_equations.remove(expected_last_bit)
            new_equations_by_op: dict[Operation, list[LogicEquation]] = defaultdict(list)
            for equation in new_equations:
                new_equations_by_op[equation.operation].append(equation)
            # Then there is one of each of XOR, AND and OR on previous wires (non-x/y inputs)
            for operation, equations in new_equations_by_op.items():
                if len(equations) == 1 and equations[0].lhs[0] not in 'xy' and equations[0].rhs[0] not in 'xy':
                    known_good_equations.add(equations[0])
                    new_equations.remove(equations[0])
            # If that's all we found, this set of equations seems fine, move on to the next bit.
            if len(new_equations) == 0:
                continue

            # Otherwise, the remaining equations are a bit sus, but they may be OK, check and see
            if test_equations(initial_equations, z_bit+1):
                log(DEBUG, f'z{z_bit:02} actually no problem, passed the test')
                known_good_equations.update(new_equations)
                continue

            # These new equations are candidates for swapping out
            log(DEBUG, f'z{z_bit:02} has new equations to check: {new_equations}')
            new_equation_results = [initial_equation_results[equation] for equation in new_equations]

            # Candidates for swapping in are any other equations that could be used here
            # Equations can only be swapped in if they rely only on up to the current number of bits
            possibilities = [
                result for result, max_bit in equation_max_bit.items()
                if max_bit <= z_bit and initial_equations[result] not in known_good_equations]
            log(DEBUG, '  possibilities: ', possibilities)
            log(DEBUG, '  possible_equations:', [
                eq for result, eq in initial_equations.items() 
                if result in possibilities], '\n')
            
            swap = find_swap(
                new_equation_results, possibilities, initial_equations, z_bit+1)
            assert swap is not None

            # Swap the equations. Also swap any data derived from them.
            swap_equations = initial_equations[swap[0]], initial_equations[swap[1]]
            initial_equations[swap[0]], initial_equations[swap[1]] = initial_equations[swap[1]], initial_equations[swap[0]]
            initial_equation_results[swap_equations[0]] = swap[1]
            initial_equation_results[swap_equations[1]] = swap[0]
            new_equations.remove(swap_equations[0])
            new_equations.add(swap_equations[1])
            swapped.extend(swap)

            known_good_equations.update(new_equations)

        z = calculate_z(dict(known_bits), initial_equations)
        log(INFO, f'Now got:  {z:045b}')
        log(INFO, f'Expected: {expected:045b}')
        log(INFO, 'Number of wrong bits', (z ^ expected).bit_count())

        swapped_wires = ','.join(sorted(swapped))
        log(RESULT, 'Wires invovled in swaps are:', swapped_wires)
        return swapped_wires


part = Part2()

part.add_result('ggn,grm,jcb,ndw,twr,z10,z32,z39')
