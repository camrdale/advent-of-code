import queue

import aoc.input
from aoc import log
from aoc import runner

from year2023.day22 import shared


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        bricks: list[shared.Brick] = []
        for i, line in enumerate(input):
            bricks.append(shared.Brick.from_text(i, line))
        
        shared.settle(bricks)

        total_falling = 0
        for brick in sorted(bricks):
            falling_bricks = brick.would_fall()
            to_fall: queue.PriorityQueue[shared.Brick] = queue.PriorityQueue()
            for falling_brick in falling_bricks:
                to_fall.put(falling_brick)
            while not to_fall.empty():
                falling_brick = to_fall.get()
                for supported_brick in falling_brick.supports - falling_bricks:
                    if supported_brick.will_fall(falling_bricks):
                        falling_bricks.add(supported_brick)
                        to_fall.put(supported_brick)
            total_falling += len(falling_bricks)
            log.log(log.INFO, f'Disintegrating brick {brick.num} would cause {len(falling_bricks)} other bricks to fall: {[b.num for b in falling_bricks]}')

        log.log(log.RESULT, f'Sum of the other bricks that would fall: {total_falling}')
        return total_falling


part = Part2()

part.add_result(7, r"""
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""")

part.add_result(69601)
