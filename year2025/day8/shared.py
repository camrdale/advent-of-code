from aoc.map import Coordinate3D
from aoc.sets import DisjointSet

from typing import NamedTuple, Self


class Connection(NamedTuple):
    distance_squared: int
    node_a: Coordinate3D
    node_b: Coordinate3D

    def __repr__(self) -> str:
        return f'{self.node_a} -> {self.node_b}'

    @classmethod
    def from_nodes(cls, node_a: Coordinate3D, node_b: Coordinate3D) -> Self:
        distance_squared = (
            (node_a.location.x - node_b.location.x) ** 2 +
            (node_a.location.y - node_b.location.y) ** 2 +
            (node_a.z - node_b.z) ** 2)
        return cls(distance_squared, node_a, node_b)

    @classmethod
    def from_input(cls, lines: list[str]) -> tuple[DisjointSet[Coordinate3D], list[Self]]:
        boxes: list[Coordinate3D] = []
        connections: list[Self] = []
        sets: DisjointSet[Coordinate3D] = DisjointSet()

        for line in lines:
            node = Coordinate3D.from_text(line)
            connections.extend(cls.from_nodes(previous_node, node) for previous_node in boxes)
            boxes.append(node)
            sets.add(node)

        connections.sort()
        return sets, connections
