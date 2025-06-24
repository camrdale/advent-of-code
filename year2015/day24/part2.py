from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day24.shared import optimal_size


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        num_packages, quantum_entanglement = optimal_size([int(line) for line in input], 4)

        log.log(log.RESULT, f'Quantum entanglement of smallest package group of size {num_packages}: {quantum_entanglement}')
        return quantum_entanglement


part = Part2()

part.add_result(44, """
1
2
3
4
5
7
8
9
10
11
""")

part.add_result(72050269)
