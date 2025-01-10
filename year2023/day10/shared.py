from aoc.input import InputParser
from aoc.log import log, INFO
from aoc.map import Coordinate, ParsedMap, Offset

PIPE_NEIGHBORS = {
    '|': (Offset(0,-1), Offset(0,1)),
    '-': (Offset(-1,0), Offset(1,0)),
    'L': (Offset(0,-1), Offset(1,0)),
    'J': (Offset(-1,0), Offset(0,-1)),
    '7': (Offset(-1,0), Offset(0,1)),
    'F': (Offset(0,1), Offset(1,0)),
    }


class PipeMap(ParsedMap):
    def __init__(self, parser: InputParser):
        super().__init__(parser.get_input(), ''.join(PIPE_NEIGHBORS.keys()) + 'S')
        self.starting_point = next(iter(self.features['S']))
        del self.features['S']
        self.features[self.starting_pipe()].add(self.starting_point)

    def starting_pipe(self) -> str:
        neighbor_offsets: list[Offset] = []
        for neighbor in self.starting_point.neighbors():
            neighbor_pipe = self.at_location(neighbor)
            if neighbor_pipe in PIPE_NEIGHBORS:
                neighbor_neighbors = PIPE_NEIGHBORS[neighbor_pipe]
                for neighbor_neighbor in neighbor_neighbors:
                    if neighbor.add(neighbor_neighbor) == self.starting_point:
                        neighbor_offsets.append(neighbor_neighbor.negate())
        neighbor_offsets_tuple = tuple(sorted(neighbor_offsets))
        log(INFO, f'Starting node neighbors are at: {neighbor_offsets_tuple}')
        assert len(neighbor_offsets_tuple) == 2
        for pipe, offsets in PIPE_NEIGHBORS.items():
            if offsets == neighbor_offsets_tuple:
                return pipe
        assert False

    def starting_nodes(self) -> list[Coordinate]:
        return [
            self.starting_point.add(offset)
            for offset in PIPE_NEIGHBORS[self.at_location(self.starting_point)]]

    def next_node(self, location: Coordinate, seen_nodes: set[Coordinate]) -> Coordinate:
        seen_nodes.add(location)
        neighbors = [location.add(offset) for offset in PIPE_NEIGHBORS[self.at_location(location)]]
        for neighbor in neighbors:
            if neighbor not in seen_nodes:
                return neighbor
        assert False

    def loop_nodes(self) -> set[Coordinate]:
        next_nodes = self.starting_nodes()
        seen_nodes = {self.starting_point}
        steps = 1
        while next_nodes[0] != next_nodes[1]:
            next_nodes[0] = self.next_node(next_nodes[0], seen_nodes)
            next_nodes[1] = self.next_node(next_nodes[1], seen_nodes)
            steps += 1
        seen_nodes.add(next_nodes[0])
        return seen_nodes
