from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day13.shared import CartMap


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        cart_map = CartMap(input)

        turn = 0
        while True:
            turn += 1
            collision = cart_map.simulate_turn()
            if collision:
                if len(cart_map.carts) == 1:
                    log.log(log.RESULT, f'The only remaining cart on turn {turn}: {cart_map.carts[0]}')
                    return f'{cart_map.carts[0].location.x},{cart_map.carts[0].location.y}'
                else:
                    log.log(log.INFO, f'Collision on turn {turn}, carts remaining: {len(cart_map.carts)}')


part = Part2()

part.add_result('6,4', r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
""")

part.add_result('21,91')
