import heapq
import itertools
from typing import NamedTuple, Any

from aoc.map import ParsedMap, Coordinate


WALL = '#'
ELF = 'E'
GOBLIN = 'G'
HIT_POINTS = 200


class Unit:
    def __init__(self, location: Coordinate, type: str, attack_power: int = 3) -> None:
        self.location = location
        self.type = type
        self.hit_points = HIT_POINTS
        self.attack_power = attack_power
    
    def attack_key(self) -> tuple[int, Coordinate]:
        """Sorting for attacking, lowest hit points first, then reading order."""
        return (self.hit_points, self.location)

    def __lt__(self, other: Any) -> bool:
        """Default sort by reading order of location, for the order than turns are taken."""
        if type(other) != Unit:
            raise ValueError(f'Unexpected {other}')
        return self.location < other.location

    def __repr__(self) -> str:
        return f'{self.type}({self.hit_points})'


class Path(NamedTuple):
    """An alternative Path for Djikstra's path finding, that will be processed in appropriate order.
    
    For shortest path ties, the reading order of the destination location breaks ties.
    For the same destination, the reading order of the first location in the previous steps breaks ties.
    """
    length: int
    location: Coordinate
    previous: tuple[Coordinate, ...]

    def first_step(self) -> Coordinate:
        return self.previous[1] if len(self.previous) > 1 else self.location
    
    def previous_step(self) -> Coordinate | None:
        if self.previous:
            return self.previous[-1]


class CaveMap(ParsedMap):
    def __init__(self, lines: list[str], elf_power: int = 3):
        super().__init__(lines, WALL + ELF + GOBLIN)
        self.units: list[Unit] = []
        for location in self.features[ELF]:
            self.units.append(Unit(location, ELF, attack_power=elf_power))
        for location in self.features[GOBLIN]:
            self.units.append(Unit(location, GOBLIN))
        self.rounds = 0

    def combat(self, abort_on_elf_death: bool = False) -> bool:
        """Run all the rounds of combat, aborting early (and returning False) if abort_on_elf_death and an elf dies."""
        while True:
            for unit in sorted(self.units):
                if unit.hit_points <= 0:
                    continue

                attacked_unit = self.attack(unit)

                if attacked_unit is None:
                    done = self.move(unit)
                    if done:
                        return True
                    attacked_unit = self.attack(unit)

                if attacked_unit is not None:
                    attacked_unit.hit_points -= unit.attack_power
                    if attacked_unit.hit_points <= 0:
                        self.features[attacked_unit.type].remove(attacked_unit.location)
                        self.units.remove(attacked_unit)
                        if abort_on_elf_death and attacked_unit.type == ELF:
                            return False

            self.rounds += 1

    def attack(self, unit: Unit) -> Unit | None:
        """Attempt an attack from the unit. Returns the unit that would be attacked, None if there are no possible attacks."""
        neighbors = set(unit.location.neighbors())
        targets = [
            enemy_unit
            for enemy_unit in self.units
            if unit.type != enemy_unit.type and enemy_unit.location in neighbors]
        if not targets:
            return None
        return sorted(targets, key=Unit.attack_key)[0]

    def next_move_paths(self, path: Path, coords_to_avoid: set[Coordinate]) -> list['Path']:
        new_previous = path.previous + (path.location,)
        return [Path(path.length + 1, neighbor, new_previous)
                for neighbor in self.neighbors(path.location)
                if neighbor != path.previous_step() and neighbor not in coords_to_avoid]

    def shortest_move(
            self, 
            starting_pos: Coordinate, 
            ending_pos: set[Coordinate],
            coords_to_avoid: set[Coordinate]
            ) -> Path | None:
        visited: dict[Coordinate, int] = {}
        paths_to_try: list[Path] = []
        heapq.heappush(paths_to_try, Path(0, starting_pos, ()))

        while paths_to_try:
            path = heapq.heappop(paths_to_try)
            if path.location in visited:
                continue
            visited[path.location] = path.length

            if path.location in ending_pos:
                # Can only visit the ending locations once, so the first time is the shortest path.
                return path

            for next_path in self.next_move_paths(path, coords_to_avoid):
                heapq.heappush(paths_to_try, next_path)

    def move(self, unit: Unit) -> bool:
        """Attempt to move the unit, returns False if there are targets for the unit."""
        targets = [enemy_unit for enemy_unit in self.units if unit.type != enemy_unit.type]
        if not targets:
            return True
        coords_to_avoid: set[Coordinate] = self.features[WALL] | self.features[ELF] | self.features[GOBLIN]
        target_locations = set(itertools.chain.from_iterable(
            target.location.neighbors() for target in targets)) - coords_to_avoid
        
        if target_locations:
            path = self.shortest_move(unit.location, target_locations, coords_to_avoid)
            if path is not None:
                self.features[unit.type].remove(unit.location)
                unit.location = path.first_step()
                self.features[unit.type].add(unit.location)

        return False

    def outcome(self) -> int:
        return self.rounds * sum(unit.hit_points for unit in self.units)
