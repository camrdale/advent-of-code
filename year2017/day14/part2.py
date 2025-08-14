from aoc.input import InputParser
from aoc import log
from aoc.runner import Part
from aoc.sets import DisjointSet

from year2017.knot_hash import knot_hash


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        rows: list[list[int]] = []
        for row in range(128):
            l = knot_hash(f'{input}-{row}')
            rows.append([n >> i & 1 for n in l for i in range(7,-1,-1)])

        # Build a disjoint set structure, using the row and column to identify the squares.
        disjoint_set = DisjointSet()
        for row in range(128):
            for column in range(128):
                if not rows[row][column]:
                    continue
                disjoint_set.add((row, column))
                if row > 0 and rows[row-1][column]:
                    disjoint_set.union((row, column), (row - 1, column))
                if column > 0 and rows[row][column-1]:
                    disjoint_set.union((row, column), (row, column - 1))

        num_groups = disjoint_set.size()

        log.log(log.RESULT, f'The number of used squares: {num_groups}')
        return num_groups


part = Part2()

part.add_result(1242, """
flqrgnkx
""")

part.add_result(1139, """
nbysizxe
""")
