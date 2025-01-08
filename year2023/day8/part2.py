import math
import re

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

NETWORK_RE = re.compile(r'([A-Z0-9]*) = \(([A-Z0-9]*), ([A-Z0-9]*)\)')


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        instructions, network_input = parser.get_two_part_input()

        starting_nodes: list[str] = []
        network: dict[str, tuple[str, str]] = {}
        for line in network_input:
            match = NETWORK_RE.match(line)
            if match is None:
                print(f'ERROR: failed to network parse: {line}')
                return -1
            source_node, left_node, right_node = match.groups()
            network[source_node] = (left_node, right_node)
            if source_node.endswith('A'):
                starting_nodes.append(source_node)

        log(INFO, f'Starting nodes: {starting_nodes}')

        steps_to_z: list[int] = []
        for starting_node in starting_nodes:
            current_node = starting_node
            steps = 0
            while not current_node.endswith('Z'):
                for instruction in instructions[0]:
                    if current_node.endswith('Z'):
                        break
                    next_nodes = network[current_node]
                    if instruction == 'L':
                        current_node = next_nodes[0]
                    else:
                        current_node = next_nodes[1]
                    steps += 1
            steps_to_z.append(steps)
            log(INFO, f'{starting_node} became {current_node} after {steps} steps')
            
        steps_to_all_z = math.lcm(*steps_to_z)
        log(RESULT, f'The steps to reach all nodes ending in Z: {steps_to_all_z}')
        return steps_to_all_z


part = Part2()

part.add_result(6, """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""")

part.add_result(9606140307013)
