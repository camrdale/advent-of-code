from aoc.map import EmptyMap, Coordinate, UP, RIGHT, DOWN, LEFT
import heapq
from typing import NamedTuple
import hashlib

from aoc import log

DIRECTIONS = {
    UP: 'U',
    DOWN: 'D',
    LEFT: 'L',
    RIGHT: 'R',
}



class Path(NamedTuple):
    length: int
    location: Coordinate
    previous: str


class VaultRooms(EmptyMap):
    def __init__(self, passcode: str):
        super().__init__(0, 0, 3, 3)
        self.passcode = passcode
        
    def next_md5_paths(self, path: Path) -> list['Path']:
        paths: list['Path'] = []
        doors = hashlib.md5((self.passcode + path.previous).encode()).hexdigest()
        for i, (offset, c) in enumerate(DIRECTIONS.items()):
            neighbor = path.location.add(offset)
            if self.valid(neighbor) and doors[i] >= 'b':
                paths.append(Path(path.length + 1, neighbor, path.previous + c))
        return paths

    def path(self, short: bool = True) -> Path:
        paths_to_try: list[Path] = []
        found_path: Path | None = None
        heapq.heappush(paths_to_try, Path(0, Coordinate(0, 0), ''))
        max_length = 0

        while paths_to_try:
            path = heapq.heappop(paths_to_try)

            if path.length > max_length:
                max_length = path.length
                log.log(log.INFO, f'{max_length}: {len(paths_to_try)}')

            if path.location == Coordinate(3, 3):
                found_path = path
                if short:
                    return found_path
                continue

            for next_path in self.next_md5_paths(path):
                heapq.heappush(paths_to_try, next_path)

        if found_path is None:
            raise ValueError(f'Failed to find a path to the vault')
        return found_path
