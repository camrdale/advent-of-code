import re

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

NETWORK_RE = re.compile(r'([A-Z]*) = \(([A-Z]*), ([A-Z]*)\)')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        instructions, network_input = parser.get_two_part_input()

        network: dict[str, tuple[str, str]] = {}
        for line in network_input:
            match = NETWORK_RE.match(line)
            if match is None:
                print(f'ERROR: failed to network parse: {line}')
                return -1
            source_node, left_node, right_node = match.groups()
            network[source_node] = (left_node, right_node)

        steps = 0
        current_node = 'AAA'
        while current_node != 'ZZZ':
            for instruction in instructions[0]:
                if current_node == 'ZZZ':
                    break
                next_nodes = network[current_node]
                if instruction == 'L':
                    current_node = next_nodes[0]
                else:
                    current_node = next_nodes[1]
                steps += 1

        log(RESULT, f'The steps to reach ZZZ: {steps}')
        return steps


part = Part1()

part.add_result(2, """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""")

part.add_result(6, """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""")

part.add_result(19241)
