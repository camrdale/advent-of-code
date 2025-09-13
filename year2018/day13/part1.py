from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day13.shared import CartMap


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        cart_map = CartMap(input)

        turn = 0
        while True:
            turn += 1
            collision = cart_map.simulate_turn()
            if collision:
                log.log(log.RESULT, f'The location if the first crash on turn {turn}: {collision[0]}')
                return f'{collision[0].x},{collision[0].y}'


part = Part1()

part.add_result('7,3', r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
""")

part.add_result('16,45')
