from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.map import Coordinate
from aoc.runner import Part

from year2023.day10.shared import PipeMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        map = PipeMap(parser)

        loop_nodes = map.loop_nodes()

        enclosed = 0
        for y in range(map.min_y, map.max_y + 1):
            inside = False
            for x in range(map.min_x, map.max_x + 1):
                location = Coordinate(x,y)
                if location in loop_nodes:
                    pipe = map.at_location(location)
                    if pipe == '|' or pipe == 'L' or pipe == 'J':
                        inside = not inside
                else:
                    if inside:
                        enclosed += 1

        log(RESULT, f'Number of tiles enclosed by the loop: {enclosed}')
        return enclosed


part = Part2()

part.add_result(4, """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""")

part.add_result(4, """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""")

part.add_result(8, """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""")

part.add_result(10, """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""")

part.add_result(413)
