from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import ReindeerMaze, Coordinate


class Part2(Part):
    def run(self, parser: InputParser) -> Coordinate | None:
        bytes = parser.get_input_coords()
        width: int
        height: int
        num_fall: int
        width, height, num_fall = parser.get_additional_params()

        maze = ReindeerMaze(width, height)

        maze.add_walls(bytes[:num_fall])

        path = maze.shortest_path()

        if path is None:
            print('ERROR failed to find initial path through the maze')
            return None

        next_to_fall = num_fall
        while next_to_fall < len(bytes):
            next_byte = bytes[next_to_fall]
            maze.add_walls((next_byte,))
            if next_byte in path.previous:
                path = maze.shortest_path()
                if path is None:
                    log(RESULT, f'Path is not possible after {next_to_fall} byte: {next_byte}')
                    return next_byte
            next_to_fall += 1


part = Part2()

part.add_result(Coordinate(6,1), """
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

part.add_result(Coordinate(22,33), None, 71, 71, 1024)
