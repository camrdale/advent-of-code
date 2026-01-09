import itertools
import re

import numpy
import numpy.typing
import scipy.optimize

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


MACHINE = re.compile(r'\[([.#]*)\] ([0-9,\(\) ]*) \{([0-9,]*)\}')


def solve_with_scipy(
        A_eq: numpy.typing.NDArray[numpy.float64],
        b_eq: numpy.typing.NDArray[numpy.float64]
        ) -> tuple[int, numpy.typing.NDArray[numpy.float64]]:
    c = numpy.ones(A_eq.shape[1])
    result = scipy.optimize.linprog(c, A_eq=A_eq, b_eq=b_eq, integrality=1)
    assert result.success, result
    assert numpy.allclose(A_eq @ result.x, b_eq, rtol=0.001, atol=0.001), f'Mismatched solution: {A_eq @ result.x} != {b_eq}'
    log.log(log.INFO, f'Found scipy solution {result.fun} with presses: {result.x}')
    return round(result.fun), result.x


def gauss_jordan(
        A: numpy.typing.NDArray[numpy.float64],
        b: numpy.typing.NDArray[numpy.float64],
        scipy_solution: numpy.typing.NDArray[numpy.float64]
        ) -> tuple[numpy.typing.NDArray[numpy.float64], numpy.typing.NDArray[numpy.float64], list[int]]:
    assert numpy.allclose(A @ scipy_solution, b, rtol=0.001, atol=0.001), f'Mismatched solution: {A @ scipy_solution} != {b}'
    A_red = A.copy()
    b_red = b.copy()
    K = b_red.shape[0]  # number of equations (rows)
    L = A_red.shape[1]  # number of unknowns (columns)
    k = 0
    l = 0
    free: list[int] = []

    while l < L and k < K:
        # Find the row with the max pivot value
        max_k = int(k + numpy.argmax(abs(A_red[k:, l])))
        if abs(A_red[max_k, l]) < 0.001:
            # No non-zero pivot values in this column, pass to next column
            free.append(l)
            l += 1
            continue

        if max_k != k:
            # Swap rows to move the max pivot value to the current row
            b_red[[k, max_k]] = b_red[[max_k, k]]
            A_red[[k, max_k]] = A_red[[max_k, k]]
            assert numpy.allclose(A_red @ scipy_solution, b_red, rtol=0.001, atol=0.001), f'Mismatched solution: {A_red @ scipy_solution} != {b_red}'

        # Divide the k-th equation by A[k,l] (normalize the pivot value to 1)
        b_red[k] /= A_red[k, l]
        A_red[k, :] /= A_red[k, l]
        assert numpy.allclose(A_red @ scipy_solution, b_red, rtol=0.001, atol=0.001), f'Mismatched solution: {A_red @ scipy_solution} != {b_red}'

        # Subtract A[i, l] times k-th equation from the i-th equation
        for i in range(K):
            if i == k:
                continue
            f = A_red[i, l]
            A_red[i, :] -= A_red[k, :] * f
            b_red[i] -= b_red[k] * f
            assert numpy.allclose(A_red @ scipy_solution, b_red, rtol=0.001, atol=0.001), f'Mismatched solution: {A_red @ scipy_solution} != {b_red}'

        # Move on to the next pivot value.
        k += 1
        l += 1

    # Remaining unknowns are all free
    for i in range(l, L):
        free.append(i)
    
    return A_red, b_red, free


def best_solution(
        A_red: numpy.typing.NDArray[numpy.float64],
        b_red: numpy.typing.NDArray[numpy.float64],
        free: list[int],
        limit: int
        ) -> numpy.typing.NDArray[numpy.float64]:
    num_unknowns = A_red.shape[1]

    # Default limits for free values comes from max joltages
    free_value_limits = [limit for _ in free]
    for equation, result in zip(A_red, b_red):
        if numpy.all(equation > -0.001):
            # Equation is all positive elements, so included free variables can't exceed result value
            for i, free_l in enumerate(free):
                if equation[free_l] > 0.001:
                    free_value_limits[i] = min(free_value_limits[i], round(result / equation[free_l]))
    
    best_x = numpy.zeros(num_unknowns)
    solution = limit * num_unknowns
    non_free = [l for l in range(num_unknowns) if l not in free]
    for free_values in itertools.product(*[range(free_value_limit + 1) for free_value_limit in free_value_limits]):
        x = numpy.zeros(num_unknowns)
        for free_l, free_value in zip(free, free_values):
            x[free_l] = free_value
        for l in non_free:
            if sum(x) >= solution:
                break
            k = numpy.argmax(A_red[:, l])
            x[l] = b_red[k]
            for free_l, free_value in zip(free, free_values):
                x[l] -= free_value * A_red[k, free_l]
        
        if sum(x) >= solution:
            continue

        if not numpy.allclose(x, numpy.round(x), rtol=0.001, atol=0.001):
            # Must be integers
            continue

        if not numpy.all(x > -0.001):
            # Must not be negative
            continue

        best_x = x
        solution = sum(x)
        log.log(log.DEBUG, f'New best solution {solution}: {x}')

    return best_x


def solve(
        A: numpy.typing.NDArray[numpy.float64],
        b: numpy.typing.NDArray[numpy.float64],
        scipy_solution: numpy.typing.NDArray[numpy.float64]
        ) -> int:
    A_red, b_red, free = gauss_jordan(A, b, scipy_solution)
    log.log(log.DEBUG, f'Reduced row echelon form\n{A_red}\n{b_red}')
    log.log(log.DEBUG, f'Free variables are: {free}')

    best_x = best_solution(A_red, b_red, free, int(max(b)))
    solution = sum(best_x)

    log.log(log.INFO, f'Found solution {solution} with presses: {best_x}')

    assert numpy.allclose(A @ best_x, b, rtol=0.001, atol=0.001), f'Mismatched solution: {A @ best_x} != {b}'

    return round(solution)


def fewest_presses(target_joltages: tuple[int, ...], buttons: list[tuple[int, ...]]) -> int:
    A = numpy.zeros((len(target_joltages), len(buttons)))
    for button_i, button in enumerate(buttons):
        for joltage_i in button:
            A[joltage_i, button_i] = 1
    b = numpy.array(target_joltages, dtype=numpy.float64)
    scipy_result, scipy_solution = solve_with_scipy(A, b)
    result = solve(A, b, scipy_solution)
    assert result == scipy_result, f'{result} != {scipy_result}'
    return scipy_result


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_presses = 0
        for line in input:
            machine = MACHINE.fullmatch(line)
            assert machine is not None, line

            buttons: list[tuple[int, ...]] = []
            for button_input in machine.group(2).split():
                buttons.append(tuple(map(int, button_input[1:-1].split(','))))
            joltages = tuple(map(int, machine.group(3).split(',')))

            num_presses = fewest_presses(joltages, buttons)
            log.log(log.INFO, f'{num_presses} presses to get joltages: {joltages}')
            total_presses += num_presses

        log.log(log.RESULT, f'The fewest total presses to configure all machines joltage levels: {total_presses}')
        return total_presses


part = Part2()

part.add_result(33, """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""")

part.add_result(22430)
