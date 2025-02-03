import aoc.map


DIRECTIONS = {
    'U': aoc.map.UP, 
    'D': aoc.map.DOWN, 
    'L': aoc.map.LEFT,
    'R': aoc.map.RIGHT}


def build_path_dict(path: list[str]) -> dict[aoc.map.Coordinate, int]:
    points: dict[aoc.map.Coordinate, int] = {}
    location = aoc.map.Coordinate(0,0)
    steps = 0
    for segment in path:
        direction = DIRECTIONS[segment[0]]
        for _ in range(int(segment[1:])):
            location = location.add(direction)
            steps += 1
            if location not in points:
                points[location] = steps
    return points
