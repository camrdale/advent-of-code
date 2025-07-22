import heapq
from typing import NamedTuple

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2016.day22.shared import Node



class Path(NamedTuple):
    length: int
    location: Coordinate


def shortest_paths(
        nodes: dict[Coordinate, Node],
        starting_pos: Coordinate, 
        ending_pos: Coordinate, 
        coords_to_avoid: set[Coordinate]
        ) -> Path:
    """Find the shortest paths from starting_pos, avoiding the coords_to_avoid."""
    visited: dict[Coordinate, int] = {}
    paths_to_try: list[Path] = []
    heapq.heappush(paths_to_try, Path(0, starting_pos))

    while paths_to_try:
        path = heapq.heappop(paths_to_try)
        if path.location in visited:
            continue
        visited[path.location] = path.length

        if path.location == ending_pos:
            return path

        for neighbor in path.location.neighbors():
            if neighbor not in nodes:
                continue
            if neighbor in coords_to_avoid:
                continue
            if nodes[neighbor].used > nodes[path.location].size:
                continue
            heapq.heappush(paths_to_try, Path(path.length + 1, neighbor))

    raise ValueError(f'Failed to find a path')



class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        zero_node: Coordinate | None = None
        nodes: dict[Coordinate, Node] = {}
        for line in input[2:]:
            node = Node.from_text(line)
            nodes[node.location] = node
            if node.used == 0:
                assert zero_node is None
                zero_node = node.location

        assert zero_node is not None
        target_node = Coordinate(max(location.x for location in nodes), 0)
        destination_node = Coordinate(0, 0)

        log.log(log.INFO, f'# of nodes: {len(nodes)}')
        log.log(log.INFO, f'Max available: {max(n.available for n in nodes.values())}')
        log.log(log.INFO, f'Max used: {max(n.used for n in nodes.values())}')
        log.log(log.INFO, f'Min used: {min(n.used for n in nodes.values())}')
        log.log(log.INFO, f'Min used > 0: {min(n.used for n in nodes.values() if n.used > 0)}')
        log.log(log.INFO, f'Max size: {max(n.size for n in nodes.values())}')
        log.log(log.INFO, f'Min size: {min(n.size for n in nodes.values())}')
        log.log(log.INFO, f'# with size >= 66T: {sum(1 for n in nodes.values() if n.size >= 66)}')
        log.log(log.INFO, f'# with size >= 100T: {sum(1 for n in nodes.values() if n.size >= 100)}')

        output = ''
        for n in nodes.values():
            if n.location.y == 0:
                log.log(log.DEBUG, output)
                output = ''
            output += f' {n.size:3d}'
        log.log(log.DEBUG, output)

        output = ''
        for n in nodes.values():
            if n.location.y == 0:
                log.log(log.DEBUG, output)
                output = ''
            output += f' {n.used:3d}'
        log.log(log.DEBUG, output)

        output = ''
        for n in nodes.values():
            if n.location.y == 0:
                log.log(log.DEBUG, output)
                output = ''
            output += f' {n.available:3d}'
        log.log(log.DEBUG, output)

        num_steps = 0
        while target_node != destination_node:
            # Move the zero node in front of the target node
            in_front = target_node._replace(x=target_node.x-1)
            path = shortest_paths(nodes, zero_node, in_front, set([target_node]))
            zero_node = in_front
            num_steps += path.length

            # Move the target node one step closer to the destination
            zero_node, target_node = target_node, zero_node
            num_steps += 1

        log.log(log.RESULT, f'The number of steps required to move the data to (0,0): {num_steps}')
        return num_steps


part = Part2()

part.add_result(7, r"""
root@testdata1# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
""")

part.add_result(249)
