import queue
from typing import NamedTuple

from aoc import log
import aoc.map

from year2019 import intcode

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


class ScaffoldMap(aoc.map.ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, SCAFFOLD + ''.join(DIRECTIONS))
        self.starting_direction, self.starting_location = self.starting_point()
        self.features[SCAFFOLD].add(self.starting_location)
        for direction in DIRECTIONS:
            if direction in self.features:
                del self.features[direction]

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
    
    def scaffold_neighbors(self, location: aoc.map.Coordinate) -> list[aoc.map.Coordinate]:
        return [neighbor for neighbor in location.neighbors() 
                if neighbor in self.features[SCAFFOLD]]

    def follow_path(self) -> list[Movement]:
        location = self.starting_location
        next_location = self.scaffold_neighbors(self.starting_location)[0]
        direction: aoc.map.Direction = next_location.direction(location)
        movements: list[Movement] = [Movement(direction, 0)]
        visited_locations: set[aoc.map.Coordinate] = set([self.starting_location])
        while True:
            offset = direction.offset()
            next_location = location.add(offset)
            if next_location in self.features[SCAFFOLD]:
                # I don't know why, but going straight through every intersection is the best path.
                location = next_location
                visited_locations.add(location)
                movements[-1] = movements[-1].increment()
                continue

            next_locations = [
                neighbor
                for neighbor in self.scaffold_neighbors(location)
                if neighbor not in visited_locations]

            if len(next_locations) == 0:
                # Found the dead-end ending point
                break
            elif len(next_locations) > 1:
                raise ValueError(f'Found an intersection? {location} {next_locations}')
            next_location = next_locations[0]
            direction = next_location.direction(location)
            movements.append(Movement(direction, 0))
        return movements


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
        if current_direction.right() == new_direction:
            return 'R'
        if current_direction.left() == new_direction:
            return 'L'
        raise ValueError(f'Cant turn from {current_direction} to {new_direction}')

    def convert_to_ascii(self, movements: list[Movement]) -> list[str | int]:
        path_movements: list[str | int] = []
        current_direction = self.map.starting_direction
        for movement in movements:
            turn = self.turn(current_direction, movement.direction)
            if turn:
                path_movements.append(turn)
            current_direction = movement.direction
            if path_movements and type(path_movements[-1]) == int:
                path_movements[-1] += movement.distance
            else:
                path_movements.append(movement.distance)
        return path_movements

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
        line = ''
        log.log(log.INFO, f'ASCII output:')
        while not ascii_output.empty():
            output = ascii_output.get_nowait()
            if output > 127:
                result = output
            else:
                if output == 10:
                    log.log(log.INFO, line)
                    line = ''
                else:
                    line += chr(output)
        return result

    def find_and_run_path(self) -> int:
        movements = self.map.follow_path()
        ascii_movements = self.convert_to_ascii(movements)
        log.log(log.INFO, f'{",".join(map(str, ascii_movements))}')
        routines = self.create_routines(ascii_movements)
        if routines is None:
            raise ValueError(f'Failed to find a routine for path')
        main, a, b, c = routines
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
