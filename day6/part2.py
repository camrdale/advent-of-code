#!/usr/bin/python

from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

INCREMENTS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0)}
STARTING_DIRECTIONS = {
    '^': UP, 
    '>': RIGHT, 
    'v': DOWN, 'V': DOWN, 
    '<': LEFT}

def tuplesum(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])

def contains_loop(obstacles: set[tuple[int, int]], pos: tuple[int, int], direction: int) -> bool:
    visited_positions_direction: set[tuple[int, int, int]] = set([pos + (direction,)])
    while True:
        next_pos = tuplesum(pos, INCREMENTS[direction])
        if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
            return False
        if next_pos in obstacles:
            direction = (direction + 1) % 4
            continue
        if next_pos + (direction,) in visited_positions_direction:
            return True

        pos = next_pos
        visited_positions_direction.add(pos + (direction,))

obstacles: set[tuple[int, int]] = set()
starting_pos: tuple[int, int] | None = None
starting_direction = -1

height = 0
width = 0
with INPUT_FILE.open() as ifp:
    # for y, line in enumerate(TEST_INPUT.split()):
    for y, line in enumerate(ifp.readlines()):
        width = len(line.strip())
        if len(line) > 0:
            height += 1
            for x, c in enumerate(line.strip()):
                if c == '.':
                    pass
                elif c == '#':
                    obstacles.add((x, y))
                elif c in STARTING_DIRECTIONS:
                    starting_pos = (x, y)
                    starting_direction = STARTING_DIRECTIONS[c]

if starting_pos is None:
    exit(1)

direction = starting_direction
current_pos = starting_pos
visited_positions = set([starting_pos])
looping_obstacles: set[tuple[int, int]] = set()
while True:
    next_pos = tuplesum(current_pos, INCREMENTS[direction])
    if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
        break
    if next_pos in obstacles:
        direction = (direction + 1) % 4
        continue

    if next_pos not in visited_positions and contains_loop(obstacles | set([next_pos]), current_pos, direction):
        looping_obstacles.add(next_pos)

    current_pos = next_pos
    visited_positions.add(current_pos)

print('Number of candidate positions to create a loop:', len(looping_obstacles))
