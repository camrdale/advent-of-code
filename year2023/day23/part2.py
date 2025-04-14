from typing import Any

import aoc.input
from aoc import log
import aoc.map
from aoc import runner


class BranchPoint:
    def __init__(self, location: aoc.map.Coordinate):
        self.location = location
        self.neighbors: dict[aoc.map.Coordinate, int] = {}

    def __eq__(self, other: Any) -> bool:
        if type(other) != BranchPoint:
            return False
        return self.location == other.location

    def __hash__(self) -> int:
        return hash(self.location)
    
    def add_neighbor(self, location: aoc.map.Coordinate, distance: int) -> None:
        if location not in self.neighbors or distance > self.neighbors[location]:
            self.neighbors[location] = distance
    
    def __str__(self) -> str:
        return f'{self.location.x},{self.location.y}'


class TrailMap(aoc.map.ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, "#")

    def valid_neighbors(self, location: aoc.map.Coordinate) -> list[aoc.map.Coordinate]:
        neighbors: list[aoc.map.Coordinate] = []
        if location in self.features['>']:
            neighbors = [location.add(aoc.map.RIGHT)]
        elif location in self.features['v']:
            neighbors = [location.add(aoc.map.DOWN)]
        elif location in self.features['<']:
            neighbors = [location.add(aoc.map.LEFT)]
        elif location in self.features['^']:
            neighbors = [location.add(aoc.map.UP)]
        else:
            neighbors = location.neighbors()
        return [neighbor for neighbor in neighbors if self.valid(neighbor) and neighbor not in self.features['#']]

    def next_branch_points(self, location: aoc.map.Coordinate) -> dict[aoc.map.Coordinate, int]:
        branch_points: dict[aoc.map.Coordinate, int] = {}
        neighbors = self.valid_neighbors(location)
        for current_location in neighbors:
            distance = 1
            previous_location = location
            next_neighbors = self.valid_neighbors(current_location)
            if previous_location in next_neighbors:
                next_neighbors.remove(previous_location)
            while len(next_neighbors) == 1:
                distance += 1
                previous_location = current_location
                current_location = next_neighbors[0]
                next_neighbors = self.valid_neighbors(current_location)
                if previous_location in next_neighbors:
                    next_neighbors.remove(previous_location)
            branch_points[current_location] = distance
        return branch_points

    def branch_points(
            self,
            starting_pos: aoc.map.Coordinate, 
            ending_pos: aoc.map.Coordinate,
            ) -> dict[aoc.map.Coordinate, BranchPoint]:
        branch_points: dict[aoc.map.Coordinate, BranchPoint] = {}
        stack: list[aoc.map.Coordinate] = [starting_pos]
        while stack:
            branch_point_location = stack.pop()
            if branch_point_location in branch_points:
                continue
            # log.log(log.DEBUG, f'Finding branch points of {branch_point_location}')
            branch_point = BranchPoint(branch_point_location)
            branch_points[branch_point_location] = branch_point
            next_branch_locations = self.next_branch_points(branch_point_location)
            for next_branch_location, distance in next_branch_locations.items():
                # log.log(log.DEBUG, f'  Found branch point at {next_branch_location}, distance {distance}, new={next_branch_location not in branch_points}')
                if next_branch_location not in branch_points:
                    stack.append(next_branch_location)
                branch_point.add_neighbor(next_branch_location, distance)

        if ending_pos not in branch_points:
            raise ValueError(f'Failed to find path from {starting_pos} to {ending_pos}')
        return branch_points


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        estimated_iterations = parser.get_additional_params()[0]

        map = TrailMap(input)

        branch_points = map.branch_points(aoc.map.Coordinate(map.min_x+1,map.min_y), aoc.map.Coordinate(map.max_x-1, map.max_y))
        log.log(log.DEBUG, f'Built map of {len(branch_points)} different branch points')
        log.log(log.DEBUG, f'Start pos neighbors: {branch_points[aoc.map.Coordinate(map.min_x+1,map.min_y)].neighbors}')
        log.log(log.DEBUG, f'End pos neighbors: {branch_points[aoc.map.Coordinate(map.max_x-1, map.max_y)].neighbors}')
        log.log(log.DEBUG, map.print_map({'X': set(branch_points.keys())}))

        stack: list[aoc.map.Path] = [aoc.map.Path(0, aoc.map.Coordinate(map.min_x+1,map.min_y), frozenset())]
        longest_path: aoc.map.Path | None = None
        with log.ProgressBar(estimated_iterations=estimated_iterations, desc='day 23,2') as progress_bar:
            while stack:
                path = stack.pop()
                progress_bar.update()

                if path.location == aoc.map.Coordinate(map.max_x-1, map.max_y):
                    log.log(log.INFO, f'Found a hike of length {path.length}')
                    if longest_path is None or path.length > longest_path.length:
                        longest_path = path
                    continue

                branch_point = branch_points[path.location]
                new_previous = path.previous.union((path.location,))
                for next_branch_point_location, distance in branch_point.neighbors.items():
                    if next_branch_point_location not in path.previous:
                        stack.append(aoc.map.Path(path.length + distance, next_branch_point_location, new_previous))

        if longest_path is None:
            raise ValueError(f'Failed to find a path to the end point')
        log.log(log.RESULT, f'Longest hike has length: {longest_path.length}')
        return longest_path.length


part = Part2()

part.add_result(154, r"""
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
""", 70)

part.add_result(6486, None, 30580294)
