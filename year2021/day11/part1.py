from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        matrix = [list(map(int, line)) for line in input]
        
        width = len(matrix[0])
        height = len(matrix)
        num_flashes = 0

        def neighbors(i: tuple[int, int]):
            return [j for j in ((i[0]-1, i[1]-1), (i[0]-1, i[1]), (i[0]-1, i[1]+1),
                                (i[0], i[1]-1), (i[0], i[1]+1),
                                (i[0]+1, i[1]-1), (i[0]+1, i[1]), (i[0]+1, i[1]+1))
                    if j[0] >= 0 and j[0] < height and j[1] >= 0 and j[1] < width
                        and matrix[j[0]][j[1]] < 10]

        for _ in range(100):
            for i0 in range(height):
                for i1 in range(width):
                    to_check = [(i0, i1)]
                    while to_check:
                        i = to_check.pop()
                        matrix[i[0]][i[1]] += 1
                        if matrix[i[0]][i[1]] == 10:
                            num_flashes += 1
                            to_check.extend(neighbors(i))

            for i0 in range(height):
                for i1 in range(width):
                    i = (i0, i1)
                    if matrix[i[0]][i[1]] > 9:
                        matrix[i[0]][i[1]] = 0

        log(RESULT, 'number of flashes after 100 steps:', num_flashes)
        return num_flashes


part = Part1()

part.add_result(1656, """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""")

part.add_result(1647)
