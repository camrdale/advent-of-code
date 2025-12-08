from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2025.day8.shared import Connection


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sets, connections = Connection.from_input(input)

        num_sets = sets.size()
        start = 0
        end = -1
        while num_sets > 1:
            end = start + num_sets - 2
            for connection in connections[start:end + 1]:
                sets.union(connection.node_a, connection.node_b)
            start = end + 1
            num_sets = sets.size()

        last_connection = connections[end]
        product_x = last_connection.node_a.location.x * last_connection.node_b.location.x
        log.log(log.RESULT, f'The product of the X coordinates of the last connection {product_x}: {last_connection}')
        return product_x


part = Part2()

part.add_result(25272, """
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
""")

part.add_result(2245203960)
