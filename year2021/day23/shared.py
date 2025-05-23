import heapq
from typing import NamedTuple

from aoc import log
from aoc.map import ParsedMap, Coordinate


ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


class Amphipod(NamedTuple):
    type: str
    location: Coordinate
    moved: bool = False

    def move(self, new_location: Coordinate) -> 'Amphipod':
        return Amphipod(self.type, new_location, True)


class State(NamedTuple):
    energy: int
    amphipods: frozenset[Amphipod]

    def next_state(self, old_amphipod: Amphipod, new_amphipod: Amphipod, steps: int) -> 'State':
        assert old_amphipod in self.amphipods
        return State(
            self.energy + steps * ENERGY[new_amphipod.type],
            (self.amphipods - {old_amphipod}) | {new_amphipod})


class BurrowMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, '#' + ''.join(ENERGY))
        amphipods: list[Amphipod] = []
        self.room_columns: set[int] = set()
        self.room_entry_row = self.max_y
        self.room_bottom_row = self.min_y
        for type in ENERGY:
            for location in self.features[type]:
                self.room_columns.add(location.x)
                if location.y < self.room_entry_row:
                    self.room_entry_row = location.y
                if location.y > self.room_bottom_row:
                    self.room_bottom_row = location.y
                amphipods.append(Amphipod(type, location))
        self.starting_state = State(0, frozenset(amphipods))
        self.destination_columns = dict(zip(ENERGY, sorted(self.room_columns)))

    def valid_destination(self, state: State, amphipod: Amphipod, destination: Coordinate) -> bool:
        if destination.x in self.room_columns:
            if destination.y < self.room_entry_row:
                # Amphipods will never stop on the space immediately outside any room.
                return False
            if destination.x != self.destination_columns[amphipod.type]:
                # Amphipods will never move from the hallway into a room unless that room is their destination room
                return False
            if not amphipod.moved:
                # Dont move around in the room, go to the hallway
                return False
            open_room_rows = set(range(self.room_entry_row, self.room_bottom_row + 1))
            for other in state.amphipods:
                if other == amphipod:
                    continue
                if other.location.x == destination.x:
                    if other.type != amphipod.type:
                        # Amphipods will never move into a destination room unless that room contains no amphipods which do not also have that room as their own destination.
                        return False
                    open_room_rows.remove(other.location.y)
            if destination.y != max(open_room_rows):
                # If moving into a destination room, move as far in as possible.
                return False
        else:
            if amphipod.moved:
                # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.
                return False
        return True

    def update_features(self, state: State):
        """Update the features with the current locations of all amphipods."""
        for type in ENERGY:
            self.features[type] = set()
        for amphipod in state.amphipods:
            self.features[amphipod.type].add(amphipod.location)

    def needs_to_move(self, amphipod: Amphipod, state: State) -> bool:
        if amphipod.location.x != self.destination_columns[amphipod.type]:
            return True
        in_room = frozenset([
            other
            for other in state.amphipods
            if other.location.x == amphipod.location.x and other.location.y >= amphipod.location.y])
        return not self.organized(in_room)
    
    def next_states(self, state: State) -> list[State]:
        next_states: list[State] = []

        for amphipod in state.amphipods:
            if not self.needs_to_move(amphipod, state):
                continue
            destinations, _ = self.shortest_paths(amphipod.location, Coordinate(0,0), '#' + ''.join(ENERGY))
            for destination, steps in destinations.items():
                if not self.valid_destination(state, amphipod, destination):
                    continue
                new_amphipod = amphipod.move(destination)
                next_state = state.next_state(amphipod, new_amphipod, steps)
                if not self.needs_to_move(new_amphipod, next_state):
                    # Moving an amphipod to a final position is always the best thing to do in a state
                    return [next_state]
                next_states.append(next_state)

        return next_states
    
    def organized(self, amphipods: frozenset[Amphipod]) -> bool:
        for amphipod in amphipods:
            if amphipod.location.x != self.destination_columns[amphipod.type]:
                return False
            if amphipod.location.y < self.room_entry_row:
                return False
        return True
    
    def organize(self, progress_bar: log.ProgressBar) -> int:
        visited: set[frozenset[Amphipod]] = set()
        states_to_try: list[State] = []
        heapq.heappush(states_to_try, self.starting_state)

        while states_to_try:
            progress_bar.update()
            state = heapq.heappop(states_to_try)
            if state.amphipods in visited:
                continue
            visited.add(state.amphipods)
            self.update_features(state)

            if self.organized(state.amphipods):
                return state.energy

            for next_state in self.next_states(state):
                heapq.heappush(states_to_try, next_state)

        raise ValueError(f'Failed to find an organization')


