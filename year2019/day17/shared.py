import collections.abc
import functools
import queue
import string
import time
from typing import NamedTuple, Any

from aoc import log
import aoc.map

from year2019 import intcode

CHARS = string.digits + string.ascii_letters

SCAFFOLD = '#'
UP = '^'
RIGHT = '>'
DOWN = 'v'
LEFT = '<'
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


class Movement(NamedTuple):
    direction: aoc.map.Direction
    distance: int

    def increment(self) -> 'Movement':
        return Movement(self.direction, self.distance + 1)

    def reverse(self) -> 'Movement':
        return Movement(self.direction.next().next(), self.distance)


class DirectedEdge(NamedTuple):
    starting_location: aoc.map.Coordinate
    ending_location: aoc.map.Coordinate
    movements: list[Movement]
    visited_locations: set[aoc.map.Coordinate]

    def reverse(self) -> 'DirectedEdge':
        return DirectedEdge(
            self.ending_location, 
            self.starting_location,
            list(movement.reverse() for movement in reversed(self.movements)),
            set(self.visited_locations))


class Intersection:
    def __init__(self, location: aoc.map.Coordinate):
        self.location = location
        self.edges: list[DirectedEdge] = []
    
    def add_neighbor(self, edge: DirectedEdge):
        self.edges.append(edge)


class Path:
    def __init__(self, location: aoc.map.Coordinate, remaining_scaffolding: set[aoc.map.Coordinate]):
        self.location = location
        self.edges: list[DirectedEdge] = []
        self.scaffolding_remaining: set[aoc.map.Coordinate] = remaining_scaffolding

    def __lt__(self, other: Any) -> bool:
        if type(other) != Path:
            raise ValueError(f'Unexpected {other}')
        if len(self.scaffolding_remaining) != len(other.scaffolding_remaining):
            return len(self.scaffolding_remaining) < len(other.scaffolding_remaining)
        return len(self.edges) < len(other.edges)
    
    def add_edge(self, edge: DirectedEdge) -> 'Path':
        remaining_scaffolding = set(self.scaffolding_remaining)
        remaining_scaffolding.discard(edge.ending_location)
        remaining_scaffolding.difference_update(edge.visited_locations)
        new_path = Path(edge.ending_location, remaining_scaffolding)
        new_path.edges = self.edges + [edge]
        return new_path
    
    def all_visited(self) -> set[aoc.map.Coordinate]:
        visited: set[aoc.map.Coordinate] = set()
        for edge in self.edges:
            visited.add(edge.starting_location)
            visited.add(edge.ending_location)
            visited.update(edge.visited_locations)
        return visited
    
    def all_edges(self) -> tuple[tuple[aoc.map.Coordinate, aoc.map.Coordinate], ...]:
        return tuple((edge.starting_location, edge.ending_location) for edge in self.edges)
    
    def __eq__(self, other: Any) -> bool:
        if type(other) != Path:
            return False
        return self.all_edges() == other.all_edges()
    
    def __hash__(self) -> int:
        return hash(self.all_edges())


class ScaffoldMap(aoc.map.ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, SCAFFOLD + ''.join(DIRECTIONS))
        self.starting_direction, self.starting_location = self.starting_point()
        self.features[SCAFFOLD].add(self.starting_location)
        for direction in DIRECTIONS:
            if direction in self.features:
                del self.features[direction]

    @functools.cache
    def intersections(self) -> set[aoc.map.Coordinate]:
        intersections: set[aoc.map.Coordinate] = set()
        for location in self.features[SCAFFOLD]:
            if len(self.scaffold_neighbors(location)) == 4:
                intersections.add(location)
        return intersections
    
    def starting_point(self) -> tuple[aoc.map.Direction, aoc.map.Coordinate]:
        if self.features[UP]:
            return aoc.map.Direction.NORTH, next(iter(self.features[UP]))
        if self.features[DOWN]:
            return aoc.map.Direction.SOUTH, next(iter(self.features[DOWN]))
        if self.features[LEFT]:
            return aoc.map.Direction.WEST, next(iter(self.features[LEFT]))
        if self.features[RIGHT]:
            return aoc.map.Direction.EAST, next(iter(self.features[RIGHT]))
        raise ValueError(f'Failed to find starting point')
    
    def ending_point(self) -> aoc.map.Coordinate:
        for location in self.features[SCAFFOLD]:
            neighbors = [
                neighbor for neighbor in location.neighbors()
                if neighbor in self.features[SCAFFOLD]]
            if len(neighbors) == 1 and location != self.starting_location:
                return location
        raise ValueError(f'Failed to find dead-end ending point.')
    
    def scaffold_neighbors(self, location: aoc.map.Coordinate) -> list[aoc.map.Coordinate]:
        return [neighbor for neighbor in location.neighbors() 
                if neighbor in self.features[SCAFFOLD]]

    def follow_path(self, location: aoc.map.Coordinate, next_location: aoc.map.Coordinate) -> DirectedEdge:
        starting_location = location
        direction = next_location.direction(location)
        movements: list[Movement] = [Movement(direction, 1)]
        visited_locations: set[aoc.map.Coordinate] = set()
        while next_location not in self.intersections():
            visited_locations.add(next_location)
            next_locations = [
                neighbor for neighbor in self.scaffold_neighbors(next_location)
                if neighbor != location]
            if len(next_locations) == 0:
                # Found the dead-end starting or ending point
                return DirectedEdge(starting_location, next_location, movements, visited_locations)
            elif len(next_locations) > 1:
                raise ValueError(f'Found a new intersection? {next_location} {next_locations}')
            location = next_location
            next_location = next_locations[0]
            direction = next_location.direction(location)
            if direction == movements[-1]:
                movements[-1] = movements[-1].increment()
            else:
                movements.append(Movement(direction, 1))
        return DirectedEdge(starting_location, next_location, movements, visited_locations)

    def build_graph(self) -> dict[aoc.map.Coordinate, Intersection]:
        intersections: dict[aoc.map.Coordinate, Intersection] = {}
        for intersection_location in list(self.intersections()) + [self.starting_location]:
            intersections[intersection_location] = Intersection(intersection_location)
            for neighbor in self.scaffold_neighbors(intersection_location):
                edge = self.follow_path(intersection_location, neighbor)
                if edge.ending_location == self.starting_location:
                    continue
                intersections[intersection_location].add_neighbor(edge)
        return intersections

    def find_paths(self) -> collections.abc.Generator[Path]:
        log.log(log.INFO, f'Total scaffolding: {len(self.features[SCAFFOLD])}')
        ending_location = self.ending_point()
        intersections = self.build_graph()
        paths_to_try: queue.PriorityQueue[Path] = queue.PriorityQueue()
        remaining_scaffolding = set(self.features[SCAFFOLD])
        remaining_scaffolding.discard(self.starting_location)
        paths_to_try.put_nowait(Path(self.starting_location, remaining_scaffolding))
        while not paths_to_try.empty():
            path = paths_to_try.get_nowait()
            if path.location == ending_location:
                missed_scaffolding = self.features[SCAFFOLD] - path.all_visited()
                if not missed_scaffolding:
                    yield path
                continue
            intersection = intersections[path.location]
            if len(intersection.edges) == 1:
                paths_to_try.put_nowait(path.add_edge(intersection.edges[0]))
            else:
                for edge in intersection.edges:
                    if path.edges and edge.ending_location == path.edges[-1].starting_location:
                        continue
                    if path.edges[-1].movements[-1].direction != edge.movements[0].direction:
                        # I don't know why, but going straight through every intersection is the correct answer.
                        continue
                    paths_to_try.put_nowait(path.add_edge(edge))
        raise ValueError(f'Failed to find a path')


class AsciiProgram:
    def __init__(self, intcode_input: list[int]):
        self.intcode_input = list(intcode_input)
        ascii = intcode.Program('ASCII', intcode_input)
        ascii_input: queue.Queue[int] = queue.Queue()
        ascii_output: queue.Queue[int] = queue.Queue()
        ascii.execute(ascii_input, ascii_output)
        ascii.join()
        map_input: list[str] = ['']
        while not ascii_output.empty():
            code = ascii_output.get_nowait()
            if code == 10:
                map_input.append('')
            else:
                map_input[-1] += chr(code)
        self.map = ScaffoldMap(map_input)

    def turn(self, current_direction: aoc.map.Direction, new_direction: aoc.map.Direction) -> str:
        if current_direction == new_direction:
            return ''
        if current_direction.next() == new_direction:
            return 'R'
        if current_direction.prev() == new_direction:
            return 'L'
        raise ValueError(f'Cant turn from {current_direction} to {new_direction}')

    def try_path(self, path: Path) -> int | None:
        if path.edges[0].starting_location != self.map.starting_location:
            raise ValueError(f'Path starts at {path.edges[0].starting_location}, not {self.map.starting_location}')
        path_movements: list[str | int] = []
        current_direction = self.map.starting_direction
        for edge in path.edges:
            for movement in edge.movements:
                turn = self.turn(current_direction, movement.direction)
                if turn:
                    path_movements.append(turn)
                current_direction = movement.direction
                if path_movements and type(path_movements[-1]) == int:
                    path_movements[-1] += movement.distance
                else:
                    path_movements.append(movement.distance)

        log.log(log.INFO, f'{",".join(map(str, path_movements))}')
        # self.draw_path(path_movements)

        result = self.create_routines(path_movements)
        if result is None:
            log.log(log.INFO, f'Failed to find a routine for path')
            return None
        main, a, b, c = result
        routine_path: list[str] = []
        for routine in main:
            if routine == 'A':
                routine_path.extend(a)
            if routine == 'B':
                routine_path.extend(b)
            if routine == 'C':
                routine_path.extend(c)
        log.log(log.INFO, f'{",".join(routine_path)}')
        
        log.log(log.INFO, f'main: {main}')
        log.log(log.INFO, f'A: {a}')
        log.log(log.INFO, f'B: {b}')
        log.log(log.INFO, f'C: {c}')
        return self.run_path(main, a, b, c)
    
    def run_path(self, main: list[str], a: list[str], b: list[str], c: list[str]) -> int:
        intcode_input = list(self.intcode_input)
        intcode_input[0] = 2
        ascii = intcode.Program('ASCII', intcode_input)
        ascii_input: queue.Queue[int] = queue.Queue()
        ascii_output: queue.Queue[int] = queue.Queue()
        ascii.execute(ascii_input, ascii_output)
        for char in ','.join(main):
            ascii_input.put(ord(char))
        ascii_input.put(10)
        for char in ','.join(a):
            ascii_input.put(ord(char))
        ascii_input.put(10)
        for char in ','.join(b):
            ascii_input.put(ord(char))
        ascii_input.put(10)
        for char in ','.join(c):
            ascii_input.put(ord(char))
        ascii_input.put(10)
        ascii_input.put(ord('n'))
        ascii_input.put(10)
        ascii.join()
        result = -1
        while not ascii_output.empty():
            result = ascii_output.get_nowait()
        return result

    def draw_path(self, path_movements: list[str | int]):
        direction = self.map.starting_direction
        location = self.map.starting_location
        visited: set[aoc.map.Coordinate] = set([location])
        log.log(log.INFO, self.map.print_map(additional_features={DIRECTIONS[direction]: set([location]), 'O': visited}))
        time.sleep(1)
        for movement in path_movements:
            if type(movement) == int:
                for _ in range(movement):
                    location = location.add(direction.offset())
                    visited.add(location)
            elif movement == 'R':
                direction = direction.next()
            elif movement == 'L':
                direction = direction.prev()
            else:
                raise ValueError(f'Unexpected movement: {movement}')
            log.log(log.INFO, self.map.print_map(additional_features={DIRECTIONS[direction]: set([location]), 'O': visited}))
            time.sleep(0.5)

    @staticmethod
    def starts_with(l1: list[int | str], l2: list[int | str]) -> bool:
        if len(l2) < len(l1):
            return False
        return all(i1 == i2 for i1, i2 in zip(l1, l2))
    
    def consume_movements(
            self, 
            routines: dict[str, list[str | int]], 
            remaining_movements: list[str | int]
            ) -> tuple[list[str], list[str | int]]:
        main: list[str] = []
        consumed = True
        while consumed:
            consumed = False
            for routine_code, routine in routines.items():
                if self.starts_with(routine, remaining_movements):
                    main.append(routine_code)
                    remaining_movements = remaining_movements[len(routine):]
                    consumed = True
        return main, remaining_movements

    def create_routines(
            self, 
            path_movements: list[str | int]
            ) -> tuple[list[str], list[str], list[str], list[str]] | None:
        remaining_movements = list(path_movements)
        for len_a in range(1, 11):
            a = remaining_movements[:len_a]
            main_a, remaining_movements_a = self.consume_movements({'A' : a}, remaining_movements)
            for len_b in range(1, min(11, len(remaining_movements_a))):
                b = remaining_movements_a[:len_b]
                main_ab, remaining_movements_ab = self.consume_movements({'A' : a, 'B': b}, remaining_movements_a)
                for len_c in range(1, min(11, len(remaining_movements_ab)+1)):
                    c = remaining_movements_ab[:len_c]
                    main_abc, remaining_movements_abc = self.consume_movements({'A' : a, 'B': b, 'C': c}, remaining_movements_ab)
                    if len(remaining_movements_abc) == 0 and len(main_a + main_ab + main_abc) <= 10:
                        return main_a + main_ab + main_abc, list(map(str, a)), list(map(str, b)), list(map(str, c))
        return None

    def find_paths(self) -> int:
        found_paths: dict[Path, int] = {}
        num_paths = 0
        for path in self.map.find_paths():
            if path not in found_paths:
                additional_features = {'+': self.map.intersections()}
                for i, edge in enumerate(path.edges):
                    additional_features[CHARS[i]] = edge.visited_locations
                log.log(log.INFO, self.map.print_map(additional_features=additional_features))
                found_paths[path] = num_paths
                num_paths += 1
                result = self.try_path(path)
                if result is not None:
                    return result
        raise ValueError(f'Failed to find a viable path')
