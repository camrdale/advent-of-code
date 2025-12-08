from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2025.day8.shared import Connection


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        num_connections = int(parser.get_additional_params()[0])

        sets, connections = Connection.from_input(input)

        for connection in connections[:num_connections]:
            sets.union(connection.node_a, connection.node_b)

        circuit_sizes = sets.sizes()
        circuit_sizes.sort(reverse=True)
        circuit_size_product = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

        log.log(log.RESULT, f'The product of the size of the 3 largest circuits: {circuit_size_product}')
        return circuit_size_product


part = Part1()

part.add_result(40, """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""", 10)

part.add_result(98696, None, 1000)
