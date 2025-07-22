import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day22.shared import Node


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        nodes: list[Node] = []
        for line in input[2:]:
            nodes.append(Node.from_text(line))

        num_viable = 0
        for node1, node2 in itertools.permutations(nodes, 2):
            if node1.used > 0 and node1.used < node2.available:
                num_viable += 1

        log.log(log.RESULT, f'The number of viable pairs of nodes: {num_viable}')
        return num_viable


part = Part1()

part.add_result(941)
