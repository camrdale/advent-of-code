from queue import PriorityQueue
import string
from typing import NamedTuple

from aoc.map import ParsedMap, Coordinate, Direction
from aoc.input import InputParser


class VisitedNode(NamedTuple):
    location: Coordinate
    direction: Direction


class HeatLossPath(NamedTuple):
    heat_loss: int
    location: Coordinate
    direction: Direction

    def visited_node(self) -> VisitedNode:
        return VisitedNode(self.location, self.direction)


class TrafficMap(ParsedMap):
    def __init__(self, parser: InputParser, min_turn_distance: int, max_turn_distance: int):
        super().__init__(parser.get_input(), string.digits)
        self.min_turn_distance = min_turn_distance
        self.max_turn_distance = max_turn_distance
        self.heat_losses: dict[Coordinate, int] = {}
        for feature, coords in self.features.items():
            self.heat_losses.update((coord, int(feature)) for coord in coords)

    def next_paths(self, path: HeatLossPath) -> list[HeatLossPath]:
        next_paths: list[HeatLossPath] = []
        heat_loss = 0
        location = path.location
        for i in range(1, self.max_turn_distance + 1):
            location = location.add(path.direction.offset())
            if location not in self.heat_losses:
                break
            heat_loss += self.heat_losses[location]
            if i >= self.min_turn_distance:
                next_paths.append(HeatLossPath(path.heat_loss + heat_loss, location, path.direction.next()))
                next_paths.append(HeatLossPath(path.heat_loss + heat_loss, location, path.direction.prev()))
        return next_paths

    def minimal_heat_loss_path(
            self, 
            starting_pos: Coordinate,
            starting_direction: Direction,
            ending_pos: Coordinate
            ) -> int:
        visited: dict[VisitedNode, int] = {}
        paths_to_try: PriorityQueue[HeatLossPath] = PriorityQueue()
        paths_to_try.put(HeatLossPath(0, starting_pos, starting_direction))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            node = path.visited_node()
            if node in visited and visited[node] <= path.heat_loss:
                continue
            visited[node] = path.heat_loss

            if path.location == ending_pos:
                return path.heat_loss

            for next_path in self.next_paths(path):
                paths_to_try.put(next_path)

        assert False
