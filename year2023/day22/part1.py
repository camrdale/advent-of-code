import aoc.input
from aoc import log
from aoc import runner

from year2023.day22 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        bricks: list[shared.Brick] = []
        for i, line in enumerate(input):
            bricks.append(shared.Brick.from_text(i, line))
        
        shared.settle(bricks)

        can_be_disintegrated = sum(brick.can_be_disentegrated() for brick in bricks)
        log.log(log.RESULT, f'Bricks that can be disintegrated: {can_be_disintegrated}')
        return can_be_disintegrated


part = Part1()

part.add_result(5, r"""
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""")

part.add_result(391)
