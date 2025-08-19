import string

from aoc import log
from aoc.map import Coordinate, Direction


def follow_route(input: list[str]) -> tuple[str, int]:
    map: dict[Coordinate, str] = {}
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            map[Coordinate(x,y)] = c

    location = Coordinate(input[0].index('|'), 0)
    direction = Direction.SOUTH
    waypoints: list[str] = []
    num_steps = 0
    while True:
        num_steps += 1
        location = location.add(direction.offset())
        c = map[location]
        if c in string.ascii_uppercase:
            waypoints.append(c)
            continue
        if c == ' ':
            log.log(log.INFO, f'End point found at {location}')
            return ''.join(waypoints), num_steps
        if c == '+':
            if map.get(location.add(direction.right().offset()), ' ') != ' ':
                direction = direction.right()
                if map.get(location.add(direction.left().offset()), ' ') != ' ':
                    raise ValueError(f'Cant determine direction to turn at {location}')
            elif map.get(location.add(direction.left().offset()), ' ') != ' ':
                direction = direction.left()
            else:
                raise ValueError(f'Cant determine direction to turn at {location}')
