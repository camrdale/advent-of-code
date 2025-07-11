from dataclasses import dataclass
import functools
import heapq
import itertools
import re
from typing import NamedTuple, Self, Any

from aoc import log


GENERATORS = re.compile(r'([a-z]+) generator')
MICROCHIPS = re.compile(r'([a-z]+)-compatible microchip')


@dataclass(frozen=True, eq=False)
class State:
    elevator: int
    floors: tuple[frozenset[str], ...]

    @classmethod
    def from_initial_floors(cls, initial_floors: list[list[str]]) -> Self:
        return cls(0, tuple(frozenset(floor) for floor in initial_floors))
    
    @staticmethod
    def safe_floor(floor: frozenset[str]) -> bool:
        if not any(item[-1] == 'G' for item in floor):
            return True

        for item in floor:
            if item[-1] == 'M' and item[0] + 'G' not in floor:
                return False

        return True
    
    def done(self) -> bool:
        for floor in self.floors[:-1]:
            if len(floor) > 0:
                return False
        return True
    
    def move_items(self, items: tuple[str, ...], to_floor: int) -> 'State | None':
        floors = list(self.floors)
        floors[self.elevator] -= set(items)
        if not self.safe_floor(floors[self.elevator]):
            return None
        floors[to_floor] |= set(items)
        if not self.safe_floor(floors[to_floor]):
            return None
        return State(to_floor, tuple(floors))
    
    def next_states(self) -> list['State']:
        next_states: list[State] = []
        if self.elevator > 0:
            can_move_one_down = False
            for items in itertools.combinations(self.floors[self.elevator], 1):
                next_state = self.move_items(items, self.elevator - 1)
                if next_state:
                    can_move_one_down = True
                    next_states.append(next_state)
            # Optimization: if you can move one item downstairs, don't bother bringing two items downstairs
            if not can_move_one_down:
                for items in itertools.combinations(self.floors[self.elevator], 2):
                    next_state = self.move_items(items, self.elevator - 1)
                    if next_state:
                        next_states.append(next_state)
        if self.elevator < len(self.floors) - 1:
            can_move_two_up = False
            for items in itertools.combinations(self.floors[self.elevator], 2):
                next_state = self.move_items(items, self.elevator + 1)
                if next_state:
                    can_move_two_up = True
                    next_states.append(next_state)
            # Optimization: if you can move two items upstairs, don't bother bringing one item upstairs
            if not can_move_two_up:
                for items in itertools.combinations(self.floors[self.elevator], 1):
                    next_state = self.move_items(items, self.elevator + 1)
                    if next_state:
                        next_states.append(next_state)

        return next_states

    # Optimization: pairs of objects are interchangeable
    @functools.cached_property
    def normalized_state(self) -> tuple[int, tuple[tuple[int, int], ...]]:
        # Location (floor) of each item.
        locations: dict[str, int] = {}
        for i, items in enumerate(self.floors):
            for item in items:
                locations[item] = i

        # The pairs of items, indicating which floor the generator and microchip are on.
        pairs: list[tuple[int, int]] = []
        for item, floor in locations.items():
            if item[-1] == 'G':
                pairs.append((floor, locations[item[0] + 'M']))

        return self.elevator, tuple(sorted(pairs))
    
    def __eq__(self, other: Any) -> bool:
        if type(other) != State:
            return False
        return self.normalized_state == other.normalized_state

    def __hash__(self) -> int:
        return hash(self.normalized_state)

    def __lt__(self, other: Any) -> bool:
        if type(other) != State:
            raise ValueError(f'Unexpected {other}')
        return self.normalized_state < other.normalized_state


class Path(NamedTuple):
    steps: int
    state: State

    def next_paths(self) -> list['Path']:
        next_paths: list[Path] = []
        for state in self.state.next_states():
            next_paths.append(Path(self.steps + 1, state))
        return next_paths


class ContainmentArea:
    def __init__(self, floors: list[str]) -> None:
        self.initial_floors: list[list[str]] = []
        for floor in floors:
            self.initial_floors.append([])
            for generator in re.findall(GENERATORS, floor):
                self.initial_floors[-1].append(generator[0].upper() + 'G')
            for microchip in re.findall(MICROCHIPS, floor):
                self.initial_floors[-1].append(microchip[0].upper() + 'M')

    def add_item(self, floor: int, item: str) -> None:
        if match := GENERATORS.search(item):
            self.initial_floors[floor].append(match.group(1)[0].upper() + 'G')
        elif match := MICROCHIPS.search(item):
            self.initial_floors[floor].append(match.group(1)[0].upper() + 'M')
        else:
            raise ValueError(f'Failed to parse: {item}')

    def shortest_path(self) -> int:
        visited: set[State] = set()
        paths_to_try: list[Path] = []
        heapq.heappush(paths_to_try, Path(0, State.from_initial_floors(self.initial_floors)))
        max_step = 0

        while paths_to_try:
            path = heapq.heappop(paths_to_try)
            if path.state in visited:
                continue
            visited.add(path.state)
            if path.steps > max_step:
                max_step = path.steps
                log.log(log.INFO, f'Step {max_step}: {len(paths_to_try)} paths to try')

            if path.state.done():
                return path.steps

            for next_path in path.next_paths():
                if next_path.state not in visited:
                    heapq.heappush(paths_to_try, next_path)

        raise ValueError(f'Failed to find a path to move all objects to the top floor')
    