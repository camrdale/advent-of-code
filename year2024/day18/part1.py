from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.runner import Part

from .shared import ReindeerMaze


class Part1(Part):
    def run(self, parser: InputParser) -> int | None:
        bytes = parser.get_input_coords()
        width: int
        height: int
        num_fall: int
        width, height, num_fall = parser.get_additional_params()

        maze = ReindeerMaze(width, height)

        maze.add_walls(bytes[:num_fall])

        path = maze.shortest_path()

        if path is None:
            print('ERROR failed to find path through the maze')
            return None

        log(DEBUG, maze.print_path(path))

        log(RESULT, 'Found shortest path with number of steps:', path.length)
        return path.length


part = Part1()

part.add_result(22, """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""", 7, 7, 12)

part.add_result(356, None, 71, 71, 1024)
