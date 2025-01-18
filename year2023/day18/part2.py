from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

DIRECTIONS = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}

class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sides: list[int] = []
        for i in range(len(input)):
            _, _, hex_input = input[i].split()
            length = int(hex_input[2:7], 16)
            direction = DIRECTIONS[hex_input[7]]
            log(INFO, f'{hex_input} = {direction} {length}')
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


part = Part2()

part.add_result(952408144115, """
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

part.add_result(129849166997110)
