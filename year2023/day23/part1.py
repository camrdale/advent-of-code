import queue

import aoc.input
from aoc import log
import aoc.map
from aoc import runner


class TrailMap(aoc.map.ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, "#<>^v")

    def valid_neighbors(self, location: aoc.map.Coordinate) -> list[aoc.map.Coordinate]:
        if location in self.features['>']:
            return [location.add(aoc.map.RIGHT)]
        if location in self.features['v']:
            return [location.add(aoc.map.DOWN)]
        if location in self.features['<']:
            return [location.add(aoc.map.LEFT)]
        if location in self.features['^']:
            return [location.add(aoc.map.UP)]
        return location.neighbors()

    def next_paths(self, path: aoc.map.Path) -> list[aoc.map.Path]:
        next_paths: list[aoc.map.Path] = []
        new_previous = path.previous.union((path.location,))
        for neighbor in self.valid_neighbors(path.location):
            if neighbor not in path.previous and self.valid(neighbor) and neighbor not in self.features['#']:
                next_paths.append(aoc.map.Path(path.length + 1, neighbor, new_previous))
        return next_paths
    
    def longest_path(
            self,
            starting_pos: aoc.map.Coordinate, 
            ending_pos: aoc.map.Coordinate,
            ) -> aoc.map.Path:
        longest_path: aoc.map.Path | None = None
        paths_to_try: queue.PriorityQueue[aoc.map.Path] = queue.PriorityQueue()
        paths_to_try.put(aoc.map.Path(0, starting_pos, frozenset()))

        while not paths_to_try.empty():
            path = paths_to_try.get()

            if path.location == ending_pos:
                longest_path = path
                log.log(log.INFO, f'Found a hike of length {path.length}')
                continue

            for next_path in self.next_paths(path):
                paths_to_try.put(next_path)

        if longest_path is None:
            raise ValueError(f'Failed to find a path to the end point')
        return longest_path


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        map = TrailMap(input)
        longest_path = map.longest_path(aoc.map.Coordinate(1,0), aoc.map.Coordinate(map.width-2, map.height-1))
        log.log(log.INFO, map.print_map({'O': set(longest_path.previous)}))

        log.log(log.RESULT, f'Longest hike has length: {longest_path.length}')
        return longest_path.length


part = Part1()

part.add_result(94, r"""
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""")

part.add_result(2178)
