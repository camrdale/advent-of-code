import math
import re

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Offset
from aoc.runner import Part


TARGET = re.compile(r'target area: x=([0-9-]*)..([0-9-]*), y=([0-9-]*)..([0-9-]*)')


class Target:
    def __init__(self, text: str):
        match = TARGET.match(text)
        assert match is not None

        self.x_min = int(match.group(1))
        self.x_max = int(match.group(2))
        self.y_min = int(match.group(3))
        self.y_max = int(match.group(4))

    def in_target(self, coord: Coordinate) -> bool:
        return self.x_min <= coord.x <= self.x_max and self.y_min <= coord.y <= self.y_max
    
    def next_velocity(self, velocity: Offset) -> Offset:
        return Offset(velocity.x - 1 if velocity.x > 0 else 0, velocity.y - 1)

    def hits_target(self, velocity: Offset) -> bool:
        location = Coordinate(0,0)
        while location.x <= self.x_max and location.y >= self.y_min:
            if self.in_target(location):
                return True
            location = location.add(velocity)
            velocity = self.next_velocity(velocity)
        return False

    def all_velocities(self) -> set[Offset]:
        velocities: set[Offset] = set()
        min_x_velocity = math.ceil((math.sqrt(8 * self.x_min + 1) - 1) / 2)
        max_y_velocity = abs(self.y_min) - 1
        for x in range(min_x_velocity, self.x_max + 1):
            for y in range(self.y_min, max_y_velocity + 1):
                velocity = Offset(x,y)
                if self.hits_target(velocity):
                    velocities.add(velocity)
        return velocities


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        target = Target(input[0])

        all_velocities = target.all_velocities()

        log.log(log.RESULT, 'The number of distinct initial velocities that hit the target:', len(all_velocities))
        return len(all_velocities)


part = Part2()

part.add_result(112, """
target area: x=20..30, y=-10..-5
""")

part.add_result(2223)
