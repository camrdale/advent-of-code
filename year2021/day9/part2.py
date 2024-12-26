import numpy

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        inputarray = [list(map(int, line)) for line in input]
        width = len(inputarray[0])
        height = len(inputarray)
    
        matrix = numpy.array(inputarray).reshape(height, width)

        basin_sizes: list[int] = []

        # Find the indexes of the first smallest entry in the matrix.
        mini = numpy.unravel_index(matrix.argmin(), matrix.shape)
        while matrix[mini] != 9:
            basin: set[tuple[numpy.intp, ...]] = set()

            # Recursive function to process the neighbors in a basin
            def tryi(i: tuple[numpy.intp, ...]):
                # Check for invalid locations.
                if i[0] < 0 or i[0] >= height or i[1] < 0 or i[1] >= width:
                    return
                # Abort recursion if edge reached, or location was already checked.
                if matrix[i] == 9:
                    return
                # New location found, add it, and mark as checked by setting to 9.
                basin.add(i)
                matrix[i] = 9
                # Now recursively try all the neighbors.
                tryi((i[0]-1, i[1]))
                tryi((i[0]+1, i[1]))
                tryi((i[0], i[1]-1))
                tryi((i[0], i[1]+1))

            # Start recursion from the current minimum in the matrix.
            tryi(mini)
            basin_sizes.append(len(basin))
            mini = numpy.unravel_index(matrix.argmin(), matrix.shape)

        basin_sizes.sort(reverse=True)
        largest_3_basins = basin_sizes[0]*basin_sizes[1]*basin_sizes[2]
        log(RESULT, "3 largest basins multipied:", largest_3_basins)
        return largest_3_basins


part = Part2()

part.add_result(1134, """
2199943210
3987894921
9856789892
8767896789
9899965678
""")

part.add_result(1038240)
