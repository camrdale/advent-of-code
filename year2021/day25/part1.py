from typing import cast

from aoc.input import InputParser
from aoc import log
from aoc.map import ParsedMap, Coordinate, DOWN, RIGHT
from aoc.runner import Part


DIRECTIONS = {'>': RIGHT, 'v': DOWN}


class SeaCucumberMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, ''.join(DIRECTIONS.keys()))

    def move(self, direction: str) -> bool:
        offset = DIRECTIONS[direction]
        sets = [self.features[feature] for feature in DIRECTIONS]
        all_cucumbers: set[Coordinate] = cast(set[Coordinate], set().union(*sets))
        new_feature: set[Coordinate] = set()
        for cucumber in self.features[direction]:
            moved = cucumber.add(offset)
            if not self.valid(moved):
                if direction == '>':
                    moved = moved._replace(x=0)
                else:
                    moved = moved._replace(y=0)
            if moved in all_cucumbers:
                new_feature.add(cucumber)
                continue
            new_feature.add(moved)
        if new_feature == self.features[direction]:
            return False
        self.features[direction] = new_feature
        return True

    def stop_moving(self) -> int:
        steps = 0
        moved = True
        while moved:
            moved = False
            if self.move('>'):
                moved = True
            if self.move('v'):
                moved = True
            steps += 1
            if steps < 10 or steps % 10 == 0:
                log.log(log.DEBUG, f'After {steps} steps:\n' + self.print_map())
        log.log(log.INFO, f'After {steps} steps:\n' + self.print_map())
        return steps


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = SeaCucumberMap(input)

        stop_moving = map.stop_moving()

        log.log(log.RESULT, f'The first step on which no sea cucumbers move: {stop_moving}')
        return stop_moving


part = Part1()

part.add_result(58, """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""")

part.add_result(441)
