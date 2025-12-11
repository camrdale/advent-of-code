import re

import numpy
import scipy.optimize

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


MACHINE = re.compile(r'\[([.#]*)\] ([0-9,\(\) ]*) \{([0-9,]*)\}')


def fewest_presses(target_joltages: tuple[int, ...], buttons: list[tuple[int, ...]]) -> int:
    c = numpy.ones(len(buttons))
    A_eq = numpy.zeros((len(target_joltages), len(buttons)))
    for button_i, button in enumerate(buttons):
        for joltage_i in button:
            A_eq[joltage_i, button_i] = 1
    b_eq = numpy.array(target_joltages)
    result = scipy.optimize.linprog(c, A_eq=A_eq, b_eq=b_eq, integrality=1)
    assert result.success, result
    return round(result.fun)


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
