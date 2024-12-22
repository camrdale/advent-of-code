from collections import defaultdict
from collections.abc import Callable, Iterable
import math
import operator
import re
from typing import NamedTuple

from aoc.log import log, DEBUG


ROBOT = re.compile(r'p\=([0-9]*),([0-9]*) v\=([-0-9]*),([-0-9]*)')


class Value2D(NamedTuple):
    x: int
    y: int

    def apply(self, op: Callable[[int, int], int], other: 'Value2D') -> 'Value2D':
        """Return a new object that is the result of applying the operator to each element of this and the other object."""
        return Value2D(*tuple(map(op, self, other)))


class Position(Value2D):
    @classmethod
    def fromValue2D(cls, val: Value2D) -> 'Position':
        return cls(val.x, val.y)

    def move(self, distance: Value2D, width: int, height: int) -> 'Position':
        """Create a new position that is distance away from this one."""
        pos = self.apply(operator.add, distance)
        return Position.fromValue2D(pos.apply(operator.mod, Value2D(width, height)))


class Velocity(Value2D):

    def distance(self, time: int) -> Value2D:
        """Determine the distance traveled in time at this velocity."""
        return self.apply(operator.mul, Value2D(time, time))


class Robot:

    def __init__(self, position: Position, velocity: Velocity, width: int, height: int):
        self.position = position
        self.velocity = velocity
        self.width = width
        self.height = height

    def simulate(self, time: int):
        self.position = self.position.move(self.velocity.distance(time), self.width, self.height)

    def quadrant(self) -> int | None:
        if self.position.x < self.width // 2:
            if self.position.y < self.height // 2:
                return 0
            elif self.position.y > self.height // 2:
                return 2
        elif self.position.x > self.width // 2:
            if self.position.y < self.height // 2:
                return 1
            elif self.position.y > self.height // 2:
                return 3
        return None


class RobotMap:

    def __init__(self, input: Iterable[str], width: int, height: int):
        self.width= width
        self.height = height
        self.robots: list[Robot] = []
        for line in input:
            if line.strip() == '':
                continue
            if match := ROBOT.match(line):
                self.robots.append(Robot(
                    Position(int(match.group(1)), int(match.group(2))),
                    Velocity(int(match.group(3)), int(match.group(4))),
                    width, height))
            else:
                print('ERROR failed to match:', line)
    
    def simulate(self, time: int):
        for robot in self.robots:
            robot.simulate(time)
    
    def safety_factor(self) -> int:
        quadrants: dict[int | None, int] = defaultdict(int)
        for robot in self.robots:
            quadrants[robot.quadrant()] += 1
            log(DEBUG, 'Robot', robot.position, 'is in quadrant', robot.quadrant())
        log(DEBUG, quadrants.items())
        return math.prod(quadrants[i] for i in range(4))
    
    def symmetric(self) -> bool:
        quadrants: dict[int | None, int] = defaultdict(int)
        for robot in self.robots:
            quadrants[robot.quadrant()] += 1
            log(DEBUG, 'Robot', robot.position, 'is in quadrant', robot.quadrant())
        log(DEBUG, quadrants.items())
        return quadrants[0] == quadrants[1] and quadrants[2] == quadrants[3]

    def line_lengths(self) -> tuple[int, int, int, int]:
        position_map: dict[Position, int] = defaultdict(int)
        for robot in self.robots:
            position_map[robot.position] += 1

        line_lengths: list[int] = []
        for y in range(self.height):
            line_length = 0
            for x in range(self.width):
                if position_map[Position(x, y)] > 0:
                    line_length += 1
                elif line_length > 0:
                    line_lengths.append(line_length)
                    line_length = 0
        for x in range(self.width):
            line_length = 0
            for y in range(self.height):
                if position_map[Position(x, y)] > 0:
                    line_length += 1
                elif line_length > 0:
                    line_lengths.append(line_length)
                    line_length = 0
        
        return tuple(sorted(line_lengths, reverse=True)[:4]) # type: ignore

    def __str__(self) -> str:
        position_map: dict[Position, int] = defaultdict(int)
        for robot in self.robots:
            position_map[robot.position] += 1
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                c = position_map[Position(x,y)]
                s += '.' if c == 0 else str(c)
            s += '\n'
        return s
