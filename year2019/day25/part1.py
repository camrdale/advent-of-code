import itertools
import re
from typing import NamedTuple, Self

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019 import intcode

DONT_TAKE = {'giant electromagnet', 'photons', 'infinite loop', 'escape pod', 'molten lava'}
DIRECTIONS = ['north', 'east', 'south', 'west']

NAME = re.compile(r'== ([a-zA-Z0-9 ]*) ==')
DOORS = re.compile(r'\nDoors here lead:\n(.*?)\n\n', re.DOTALL)
ITEMS = re.compile(r'\nItems here:\n(.*?)\n\n', re.DOTALL)
CHECKPOINT = re.compile(r'In the next room, a pressure-sensitive floor will verify your identity.')
TOO_HEAVY = re.compile(r'Droids on this ship are lighter than the detected value')
TOO_LIGHT = re.compile(r'Droids on this ship are heavier than the detected value')
JUST_RIGHT = re.compile(r'Analysis complete! You may proceed')
MOVE_ERROR = re.compile(r'You can\'t go that way')
TAKE_ERROR = re.compile(r'You don\'t see that item here.')
DROP_ERROR = re.compile(r'You don\'t have that item.')
PASSWORD = re.compile(r'You should be able to get in by typing ([0-9]*) on the keypad at the main airlock')


def reverse_direction(direction: str) -> str:
    return DIRECTIONS[(DIRECTIONS.index(direction) + 2) % 4]


class Path(NamedTuple):
    directions: tuple[str, ...]

    def add_direction(self, direction : str) -> 'Path':
        opposite_direction = reverse_direction(direction)
        if len(self.directions) > 0 and opposite_direction == self.directions[-1]:
            return Path(self.directions[:-1])
        return Path(self.directions + (direction,))
    
    def directions_to_path(self, path: 'Path') -> list[str]:
        """Return the direction commands to get from this path's location, to the other path's."""
        directions: list[str] = []
        different = 0
        while (len(self.directions) > different and len(path.directions) > different
               and self.directions[different] == path.directions[different]):
            different += 1
        for direction in self.directions[:(different-1 if different >0 else None):-1]:
            directions.append(reverse_direction(direction))
        for direction in path.directions[different:]:
            directions.append(direction)
        return directions


class Room(NamedTuple):
    name: str
    location: Path
    doors: tuple[str, ...]
    initial_items: tuple[str, ...]

    @classmethod
    def from_text(cls, location: Path, text: str) -> Self:
        match = NAME.search(text)
        if match is None:
            raise ValueError(f'Failed to find name of room in:\n{text}')
        name = match.group(1)
        match = DOORS.search(text)
        if match is None:
            raise ValueError(f'Failed to find doors in:\n{text}')
        doors = tuple(s[2:] for s in match.group(1).split('\n'))
        items = ()
        match = ITEMS.search(text)
        if match is not None:
            items = tuple(s[2:] for s in match.group(1).split('\n'))
        return cls(name, location, doors, items)


class Droid:
    def __init__(self, intcode_input: list[int]):
        self.program = intcode.SynchronousProgram('DROID', intcode_input)
        self.location: Path = Path(())
        self.inventory: set[str] = set()
        self.num_moves = 0
        self.num_drops = 0
        self.num_takes = 0
    
    def move(self, direction: str) -> None:
        self.num_moves += 1
        self.program.write_ascii(f'{direction}\n')
        move_text = self.program.get_latest_output_ascii()
        log.log(log.DEBUG, move_text)
        if MOVE_ERROR.search(move_text):
            raise ValueError(f'DROID failed to move in that direction')

    def move_to(self, new_location: Path) -> None:
        for direction in self.location.directions_to_path(new_location):
            self.move(direction)
            if self.program.is_done():
                raise ValueError(f'DROID exited early while moving')
        self.location = new_location

    def take(self, item: str) -> None:
        self.num_takes += 1
        self.program.write_ascii(f'take {item}\n')
        take_text = self.program.get_latest_output_ascii()
        log.log(log.DEBUG, take_text)
        if self.program.is_done():
            raise ValueError(f'DROID exited early when picking up {item}.')
        if TAKE_ERROR.search(take_text):
            raise ValueError(f'DROID failed to take {item}')
        self.inventory.add(item)

    def drop(self, item: str) -> None:
        self.num_drops += 1
        self.program.write_ascii(f'drop {item}\n')
        drop_text: str = self.program.get_latest_output_ascii()
        log.log(log.DEBUG, drop_text)
        if self.program.is_done():
            raise ValueError(f'DROID exited early when dropping {item}.')
        if DROP_ERROR.search(drop_text):
            raise ValueError(f'DROID failed to drop {item}')
        self.inventory.remove(item)
    
    def make_inventory(self, items: set[str]) -> None:
        for item in self.inventory - items:
            self.drop(item)
        for item in items - self.inventory:
            self.take(item)

    def try_items(self, items: set[str], checkpoint_direction: str) -> int:
        self.make_inventory(set(items))
        self.move(checkpoint_direction)
        checkpoint_text = self.get_last_status()
        if TOO_HEAVY.search(checkpoint_text):
            return 1
        if TOO_LIGHT.search(checkpoint_text):
            return -1
        if not JUST_RIGHT.search(checkpoint_text):
            raise ValueError(f'Expected an indication of success or failure')
        log.log(log.INFO, f'The correct combination of items: {items}')
        return 0
        
    def get_last_status(self) -> str:
        return self.program.get_latest_output_ascii()
    
    def get_password(self) -> int:
        match = PASSWORD.search(self.get_last_status())
        if match is None:
            raise ValueError(f'Failed to find password in final room status')
        return int(match.group(1))


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        aoc_input = parser.get_input()
        intcode_input = list(map(int, aoc_input[0].split(',')))

        droid = Droid(intcode_input)

        visited: set[Path] = set()
        to_investigate: list[Path] = [Path(())]
        rooms: dict[Path, Room] = {}
        # Checkpoints: [(path to checkpoint room, direction to pressure-sensitive floor)]
        checkpoints: list[tuple[Path, str]] = []

        while to_investigate:
            next_location = to_investigate.pop()
            if next_location in visited:
                continue
            visited.add(next_location)

            droid.move_to(next_location)

            room_text = droid.get_last_status()
            log.log(log.DEBUG, room_text)
            if droid.location not in rooms:
                room = Room.from_text(droid.location, room_text)
                rooms[droid.location] = room
                for item in room.initial_items:
                    if item not in DONT_TAKE:
                        droid.take(item)
                unvisited_paths = [
                    room.location.add_direction(door)
                    for door in room.doors
                    if room.location.add_direction(door) not in visited]
                if CHECKPOINT.search(room_text):
                    if len(unvisited_paths) != 1:
                        raise ValueError(f'Found multiple checkpoint doors in room')
                    checkpoints.append((droid.location, unvisited_paths[0].directions[-1]))
                else:
                    to_investigate.extend(unvisited_paths)

        log.log(log.INFO, f'All Items: {droid.inventory}')
        log.log(log.INFO, f'Checkpoints found: {checkpoints}')

        if len(checkpoints) != 1:
            raise ValueError(f'Expected 1 checkpoint, found: {checkpoints}')
        
        checkpoint_location, checkpoint_direction = checkpoints[0]
        droid.move_to(checkpoint_location)
        if not CHECKPOINT.search(droid.get_last_status()):
            raise ValueError(f'DROID failed to return to the checkpoint')

        all_items = sorted(droid.inventory)
        num_items_to_try = set(range(0, len(all_items) + 1))
        num_items = len(all_items) // 2
        num_attempts = 0
        num_num_items = 0
        while num_items_to_try:
            num_items_to_try.remove(num_items)
            num_num_items += 1
            num_too_heavy = 0
            num_too_light = 0
            for items in itertools.combinations(all_items, num_items):
                num_attempts += 1
                result = droid.try_items(set(items), checkpoint_direction)
                if result == 1:
                    num_too_heavy += 1
                    continue
                if result == -1:
                    num_too_light += 1
                    continue
                log.log(log.INFO, f'Number of moves={droid.num_moves} takes={droid.num_takes} drops={droid.num_drops}')
                password = droid.get_password()
                log.log(log.RESULT, f'Password for the main airlock: {password}')
                return password

            if not num_items_to_try:
                break
            log.log(log.INFO, f'Finished trying all combinations of length {num_items}: too_heavy={num_too_heavy}, too_light={num_too_light}')
            if num_too_heavy > num_too_light:
                next_num_items = [num for num in num_items_to_try if num < num_items]
                if next_num_items:
                    num_items = max(next_num_items)
                else:
                    num_items = min(num_items_to_try)
            else:
                next_num_items = [num for num in num_items_to_try if num > num_items]
                if next_num_items:
                    num_items = min(next_num_items)
                else:
                    num_items = max(num_items_to_try)

        raise ValueError(f'Failed to find the correct combination of items in: {all_items}')


part = Part1()

part.add_result(2147502592)
