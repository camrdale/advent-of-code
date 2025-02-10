import collections
import itertools

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2019.day10 import shared


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        asteroid_map = aoc.map.ParsedMap(input, '#')
        asteroids = asteroid_map.features['#']

        visible: dict[aoc.map.Coordinate, set[shared.NormalizedDirection]] = collections.defaultdict(set)
        for asteroid1, asteroid2 in itertools.combinations(asteroids, 2):
            direction = shared.NormalizedDirection.from_offset(asteroid2.difference(asteroid1))
            visible[asteroid1].add(direction)
            visible[asteroid2].add(direction.negate())

        most_visible = max([(len(can_see), asteroid) for asteroid, can_see in visible.items()])
        log.log(log.INFO, f'The monitoring station at {most_visible[1]} can see {most_visible[0]} asteroids')

        monitoring_station = most_visible[1]
        asteroids.remove(monitoring_station)

        # Dictionary of directions to the asteroids encountered that way (including their distance)
        directions: dict[shared.NormalizedDirection, list[tuple[int, aoc.map.Coordinate]]] = collections.defaultdict(list)
        for asteroid in asteroids:
            offset = asteroid.difference(monitoring_station)
            direction = shared.NormalizedDirection.from_offset(offset)
            distance = offset.manhattan_distance()
            directions[direction].append((distance, asteroid))

        # Sort the lists of asteroids in each direction by distance, nearest last.
        for direction_list in directions.values():
            direction_list.sort(reverse=True)

        # List of directions and asteroids in that direction, now sorted by angle.
        directions_list = sorted(directions.items())
        empty = False
        num_vaporized = 0
        while not empty:
            empty = True
            for _, direction_list in directions_list:
                if direction_list:
                    empty = False
                    # Remove the last (nearest) asteroid from the list in this direction.
                    _, asteroid = direction_list.pop()
                    num_vaporized += 1
                    if num_vaporized == 200:
                        log.log(log.RESULT, f'The 200th asteroid to be vaporized is at: {asteroid}')
                        return asteroid.x*100 + asteroid.y

        raise ValueError(f'Failed to find a 200th asteroid to vaporize.')


part = Part2()

part.add_result(802, r"""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""")

part.add_result(815)
