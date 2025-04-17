import collections.abc
from typing import NamedTuple

from aoc import log
from aoc.map import Coordinate, Offset, EmptyMap, LEFT, RIGHT


ROCK = '#'
DOWN = Offset(0, -1)
JETS = {'>': RIGHT, '<': LEFT}


class Rock(NamedTuple):
    coords: tuple[Coordinate, ...]

    def add(self, offset: Offset) -> 'Rock':
        return Rock(tuple(map(Coordinate.add, self.coords, [offset]*5)))


ROCKS = [
    Rock((Coordinate(2,0), Coordinate(3,0), Coordinate(4,0), Coordinate(5,0))),
    Rock((Coordinate(2,1), Coordinate(3,0), Coordinate(3,1), Coordinate(3,2), Coordinate(4,1))),
    Rock((Coordinate(2,0), Coordinate(3,0), Coordinate(4,0), Coordinate(4,1), Coordinate(4,2))),
    Rock((Coordinate(2,0), Coordinate(2,1), Coordinate(2,2), Coordinate(2,3))),
    Rock((Coordinate(2,0), Coordinate(2,1), Coordinate(3,0), Coordinate(3,1)))]


class TetrisMap(EmptyMap):
    def __init__(self, jet_pattern: str):
        super().__init__(0, 0, 6, 10, save_features=ROCK)
        self.jet_pattern = jet_pattern
        self.next_jet = 0
        self.highest_rock = -1
        self.rock_num = 0
        self.repeating_rock_index = None
    
    def get_jet(self) -> Offset:
        jet = JETS[self.jet_pattern[self.next_jet]]
        self.next_jet = (self.next_jet + 1) % len(self.jet_pattern)
        return jet

    def move_rock(self, rock: Rock, movement: Offset) -> Rock | None:
        moved_rock = rock.add(movement)
        if any(not self.valid(coord) for coord in moved_rock.coords):
            return None
        if any(coord in self.features[ROCK] for coord in moved_rock.coords):
            return None
        return moved_rock

    def drop_rock(self, rock: Rock):
        while True:
            # Pushed by a jet
            moved_rock = self.move_rock(rock, self.get_jet())
            if moved_rock is not None:
                rock = moved_rock
            
            # Falling one unit down
            moved_rock = self.move_rock(rock, DOWN)
            if moved_rock is None:
                break
            rock = moved_rock
        
        self.highest_rock = max(self.highest_rock, max(coord.y for coord in rock.coords))
        for coord in rock.coords:
            self.add_feature(ROCK, coord)

    def simulate(self, num_rocks: int) -> int:
        while self.rock_num < num_rocks:
            self.max_y = self.highest_rock + 10
            rock = ROCKS[self.rock_num % len(ROCKS)].add(Offset(0, self.highest_rock + 4))
            self.drop_rock(rock)
            self.rock_num += 1
        return self.highest_rock + 1

    def simulate_by_repetition(self, num_rocks: int) -> int:
        # Numbers here work for the input.txt file, and were found by manual cycle detection
        # at times when the input file repeats.
        assert num_rocks > 1709 + 1705

        height_at_1709 = self.simulate(1709)
        log.log(log.INFO, f'After 1709 rocks, the height is: {height_at_1709}')
        log.log(log.DEBUG, self.print_top_of_map(20))

        height_at_1709_plus_1705 = self.simulate(1709 + 1705)
        height_increase_every_1705 = height_at_1709_plus_1705 - height_at_1709
        log.log(log.INFO, f'After 1709+1705={1709+1705} rocks, the height is {height_at_1709_plus_1705}, an increase of {height_increase_every_1705}')
        log.log(log.DEBUG, self.print_top_of_map(20))

        num_repetitions_of_1705 = (num_rocks - 1709 - 1705) // 1705
        height_increase_for_1705_repetitions = height_increase_every_1705 * num_repetitions_of_1705
        rocks_remaining = (num_rocks - 1709 - 1705) % 1705
        log.log(log.INFO, f'To get to {num_rocks} will require {num_repetitions_of_1705} additional repetitions of the 1705 rocks, adding {height_increase_for_1705_repetitions} to the height')

        height_increase_for_rocks_remaining = self.simulate(1709 + 1705 + rocks_remaining) - height_at_1709_plus_1705
        log.log(log.INFO, f'The remaining {rocks_remaining} to get to {num_rocks} add {height_increase_for_rocks_remaining} to the height')
        log.log(log.DEBUG, self.print_top_of_map(20))

        return height_at_1709_plus_1705 + height_increase_for_1705_repetitions + height_increase_for_rocks_remaining
    
    def print_map(
            self, 
            additional_features: collections.abc.Mapping[str, collections.abc.Set[Coordinate]] | None = None, 
            additional_feature_priority: bool = True) -> str:
        s= super().print_map(
            additional_features=additional_features,
            additional_feature_priority=additional_feature_priority)
        lines = s.split('\n')
        return '\n'.join(lines[::-1])

    def print_top_of_map(self, rows: int) -> str:
        s = ''
        for y in range(self.max_y, self.max_y - rows, -1):
            for x in range(self.min_x, self.max_x + 1):
                s += self.print_coordinate(Coordinate(x,y), {}, False)
            s += '\n'
        return s
