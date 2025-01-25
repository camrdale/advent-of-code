import queue
from typing import NamedTuple, Any

import graphviz

import aoc.input
from aoc import log
from aoc import runner


class Component:
    def __init__(self, name: str):
        self.name = name
        self.neighbors: set[str] = set()

    def add_neighbor(self, neighbor: str):
        self.neighbors.add(neighbor)

    def __eq__(self, other: Any) -> bool:
        if type(other) != Component:
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Edge(NamedTuple):
    first_component: str
    second_component: str

    @classmethod
    def from_components(cls, first_component: str, second_component: str) -> 'Edge':
        first_component, second_component = sorted([first_component, second_component])
        return cls(first_component, second_component)


class Path(NamedTuple):
    length: int
    location: str
    edges: frozenset[Edge]

    def next_paths(self, components: dict[str, Component]) -> list['Path']:
        next_paths: list[Path] = []
        for neighbor in components[self.location].neighbors:
            edge = Edge.from_components(self.location, neighbor)
            if edge not in self.edges:
                next_paths.append(Path(self.length + 1, neighbor, self.edges.union((edge,))))
        return next_paths


def furthest_nodes(
        starting_node: str,
        components: dict[str, Component],
        ) -> list[str]:
    furthest_nodes: list[str] = []
    visited: set[str] = set()
    paths_to_try: queue.PriorityQueue[Path] = queue.PriorityQueue()
    path = Path(0, starting_node, frozenset())
    paths_to_try.put(path)

    while not paths_to_try.empty():
        path = paths_to_try.get()

        if path.location in visited:
            continue
        visited.add(path.location)
        if path.location != starting_node:
            furthest_nodes.append(path.location)

        for next_path in path.next_paths(components):
            paths_to_try.put(next_path)

    log.log(log.DEBUG, f'Found a longest path from {starting_node} to {path.location} of length {path.length}')
    return furthest_nodes[::-1]


def shortest_path(
        starting_node: str,
        ending_node: str,
        components: dict[str, Component],
        ) -> Path | None:
    visited: set[str] = set()
    paths_to_try: queue.PriorityQueue[Path] = queue.PriorityQueue()
    path = Path(0, starting_node, frozenset())
    paths_to_try.put(path)

    while not paths_to_try.empty():
        path = paths_to_try.get()

        if path.location in visited:
            continue
        visited.add(path.location)

        if path.location == ending_node:
            log.log(log.DEBUG, f'Found a shortest path from {starting_node} to {ending_node} of length {path.length}')
            return path

        for next_path in path.next_paths(components):
            paths_to_try.put(next_path)

    log.log(log.DEBUG, f'Found no paths from {starting_node} to {ending_node}')
    return None

def num_connected_nodes(
        starting_node: str,
        components: dict[str, Component],
        ) -> int:
    visited: set[str] = set()
    paths_to_try: queue.PriorityQueue[Path] = queue.PriorityQueue()
    path = Path(0, starting_node, frozenset())
    paths_to_try.put(path)
    
    while not paths_to_try.empty():
        path = paths_to_try.get()

        if path.location in visited:
            continue
        visited.add(path.location)

        for next_path in path.next_paths(components):
            paths_to_try.put(next_path)

    return len(visited)


def try_to_partition(
        starting_node: str,
        ending_node: str,
        components: dict[str, Component]
    ) -> bool:
    log.log(log.DEBUG, f'Trying to partition graph between {starting_node} and {ending_node}')
    shortest_path1 = shortest_path(starting_node, ending_node, components)
    if shortest_path1 is None:
        raise ValueError(f'Failed to find a first path from {starting_node} to {ending_node}')
    for edge in shortest_path1.edges:
        components[edge.first_component].neighbors.remove(edge.second_component)
        components[edge.second_component].neighbors.remove(edge.first_component)

    shortest_path2 = shortest_path(starting_node, ending_node, components)
    if shortest_path2 is None:
        raise ValueError(f'Failed to find a second path from {starting_node} to {ending_node}')
    for edge in shortest_path2.edges:
        components[edge.first_component].neighbors.remove(edge.second_component)
        components[edge.second_component].neighbors.remove(edge.first_component)

    shortest_path3 = shortest_path(starting_node, ending_node, components)
    if shortest_path3 is None:
        raise ValueError(f'Failed to find a third path from {starting_node} to {ending_node}')
    for edge in shortest_path3.edges:
        components[edge.first_component].neighbors.remove(edge.second_component)
        components[edge.second_component].neighbors.remove(edge.first_component)

    shortest_path4 = shortest_path(starting_node, ending_node, components)
    if shortest_path4 is not None:
        log.log(log.INFO, f'Failed to partition graph between {starting_node} and {ending_node}')
        return False
    log.log(log.INFO, f'Successfully partitioned graph between {starting_node} and {ending_node}')
    return True    


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        dot = graphviz.Graph(name='components', engine='neato')

        num_edges = 0
        components: dict[str, Component] = {}
        for line in input:
            component_name, neighbors = line.split(':')
            if component_name not in components:
                dot.node(component_name)
                components[component_name] = Component(component_name)
            for neighbor_name in neighbors.split():
                if neighbor_name not in components:
                    dot.node(component_name)
                    components[neighbor_name] = Component(neighbor_name)
                num_edges += 1
                components[component_name].add_neighbor(neighbor_name)
                components[neighbor_name].add_neighbor(component_name)
                dot.edge(component_name, neighbor_name)

        min_edges = 10000000
        max_edges = 0
        for component in components.values():
            if len(component.neighbors) < min_edges:
                min_edges = len(component.neighbors)
            if len(component.neighbors) > max_edges:
                max_edges = len(component.neighbors)

        log.log(log.DEBUG, f'Built a graph with {len(components)} nodes and {num_edges} edges, edges per node are {min_edges}-{max_edges}')
        dot.render()

        for starting_node in components:
            for ending_node in furthest_nodes(starting_node, components):
                partitioned_components = dict(components)
                if not try_to_partition(starting_node, ending_node, partitioned_components):
                    continue

                nodes_starting = num_connected_nodes(starting_node, components)
                nodes_other = num_connected_nodes(ending_node, components)

                log.log(log.RESULT, f'Partitioned graph has {nodes_starting}x{nodes_other}: {nodes_starting*nodes_other}')
                return nodes_starting*nodes_other

        raise ValueError('Failed to find two nodes on either side of the partition.')


part = Part1()

part.add_result(54, r"""
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
""")

part.add_result(600225)
