from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2021.day13.shared import fold


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        dot_input, fold_input = parser.get_two_part_input()

        dots: set[Coordinate] = set()
        for coords_input in dot_input:
            dots.add(Coordinate(*map(int, coords_input.split(','))))
        
        for line in fold_input:
            dots = fold(dots, line)

        max_x = max(coord.x for coord in dots)
        max_y = max(coord.y for coord in dots)
        output = ''
        for y in range(0, max_y+1):
            for x in range(0, max_x+1):
                output += '\u2588' if Coordinate(x,y) in dots else ' '
            output += '\n'

        log.log(log.RESULT, f'The characters after the folding:\n{output}')
        return output


part = Part2()

part.add_result("""█████
█   █
█   █
█   █
█████
""", """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""")

part.add_result("""███  ████ ████   ██ █  █ ███  ████ ████
█  █    █ █       █ █  █ █  █ █       █
█  █   █  ███     █ ████ █  █ ███    █ 
███   █   █       █ █  █ ███  █     █  
█    █    █    █  █ █  █ █ █  █    █   
█    ████ █     ██  █  █ █  █ █    ████
""")
