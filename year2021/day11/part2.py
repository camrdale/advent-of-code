from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        matrix = [list(map(int, line)) for line in input]
        
        width = len(matrix[0])
        height = len(matrix)

        def neighbors(i: tuple[int, int]):
            return [j for j in ((i[0]-1, i[1]-1), (i[0]-1, i[1]), (i[0]-1, i[1]+1),
                                (i[0], i[1]-1), (i[0], i[1]+1),
                                (i[0]+1, i[1]-1), (i[0]+1, i[1]), (i[0]+1, i[1]+1))
                    if j[0] >= 0 and j[0] < height and j[1] >= 0 and j[1] < width
                        and matrix[j[0]][j[1]] < 10]

        step = 0
        while(True):
            step += 1
            for i0 in range(height):
                for i1 in range(width):
                    to_check = [(i0, i1)]
                    while to_check:
                        i = to_check.pop()
                        matrix[i[0]][i[1]] += 1
                        if matrix[i[0]][i[1]] == 10:
                            to_check.extend(neighbors(i))

            num_reset = 0
            for i0 in range(height):
                for i1 in range(width):
                    i = (i0, i1)
                    if matrix[i[0]][i[1]] > 9:
                        matrix[i[0]][i[1]] = 0
                        num_reset += 1
            if num_reset == height*width:
               break

        log(RESULT, 'synchronized flash at step:', step)
        return step


part = Part2()

part.add_result(195, """
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

part.add_result(348)
