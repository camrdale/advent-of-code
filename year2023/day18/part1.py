from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sides: list[int] = []
        for i in range(len(input)):
            direction, length_input, _ = input[i].split()
            length = int(length_input)
            if direction in 'UL':
                length = -length
            sides.append(length)

        circumference = 0
        x = 0
        enclosed_area = 0
        for i in range(0, len(sides), 2):
            circumference += abs(sides[i]) + abs(sides[i+1])
            x += sides[i]
            enclosed_area += x * sides[i+1]
            log(DEBUG, f'Cubic meters of laval held so far: {enclosed_area}  (circumference is {circumference}, x is {x}, change {x * sides[i+1]})')

        area = abs(enclosed_area) + (circumference // 2) + 1
        log(RESULT, f'Cubic meters of laval held: {area}')
        return area


part = Part1()

part.add_result(9, """
R 2 (#70c710)
D 2 (#0dc571)
L 2 (#5713f0)
U 2 (#caa173)
""")

part.add_result(9, """
L 2 (#5713f0)
D 2 (#0dc571)
R 2 (#70c710)
U 2 (#caa173)
""")

part.add_result(8, """
R 1 (#70c710)
D 1 (#0dc571)
R 1 (#5713f0)
D 1 (#caa173)
L 2 (#5713f0)
U 2 (#caa173)
""")

part.add_result(8, """
L 1 (#70c710)
D 2 (#0dc571)
R 2 (#5713f0)
U 1 (#caa173)
L 1 (#5713f0)
U 1 (#caa173)
""")

part.add_result(23, """
R 4 (#70c710)
D 1 (#0dc571)
L 2 (#5713f0)
D 2 (#caa173)
R 2 (#5713f0)
D 1 (#caa173)
L 4 (#5713f0)
U 4 (#caa173)
""")

part.add_result(23, """
L 4 (#70c710)
D 4 (#0dc571)
R 4 (#5713f0)
U 1 (#caa173)
L 2 (#5713f0)
U 2 (#caa173)
R 2 (#5713f0)
U 1 (#caa173)
""")

part.add_result(69, """
R 2 (#70c710)
D 2 (#0dc571)
R 2 (#5713f0)
U 2 (#caa173)
R 2 (#5713f0)
D 4 (#caa173)
L 2 (#5713f0)
D 2 (#caa173)
R 2 (#5713f0)
D 4 (#caa173)
L 2 (#70c710)
U 2 (#0dc571)
L 2 (#5713f0)
D 2 (#caa173)
L 2 (#5713f0)
U 4 (#caa173)
R 2 (#5713f0)
U 2 (#caa173)
L 2 (#5713f0)
U 4 (#caa173)
""")

part.add_result(69, """
L 2 (#70c710)
D 2 (#0dc571)
L 2 (#5713f0)
U 2 (#caa173)
L 2 (#5713f0)
D 4 (#caa173)
R 2 (#5713f0)
D 2 (#caa173)
L 2 (#5713f0)
D 4 (#caa173)
R 2 (#70c710)
U 2 (#0dc571)
R 2 (#5713f0)
D 2 (#caa173)
R 2 (#5713f0)
U 4 (#caa173)
L 2 (#5713f0)
U 2 (#caa173)
R 2 (#5713f0)
U 4 (#caa173)
""")

part.add_result(62, """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""")

part.add_result(40714)
