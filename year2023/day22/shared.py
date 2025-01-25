import collections
from typing import Any

from aoc import log
import aoc.map


class Brick:
    def __init__(self, num: int, coord1: aoc.map.Coordinate3D, coord2: aoc.map.Coordinate3D):
        self.num = num
        self.lower_coord, self.upper_coord = sorted([coord1, coord2])
        self.rests_on: set[Brick] = set()
        self.supports: set[Brick] = set()

    @classmethod
    def from_text(cls, num:int, text: str) -> 'Brick':
        coord1_input, coord2_input = text.split('~')
        return cls(num, aoc.map.Coordinate3D.from_text(coord1_input), aoc.map.Coordinate3D.from_text(coord2_input))

    def __lt__(self, other: Any) -> bool:
        if type(other) != Brick:
            raise ValueError(f'Unexpected {other}')
        return self.lower_coord < other.lower_coord

    def __eq__(self, other: Any) -> bool:
        if type(other) != Brick:
            return False
        return self.num == other.num

    def __hash__(self) -> int:
        return hash(self.num)
        
    def coordinates(self) -> list[aoc.map.Coordinate]:
        coords: list[aoc.map.Coordinate] = []
        x1, x2 = sorted([self.lower_coord.location.x, self.upper_coord.location.x])
        y1, y2 = sorted([self.lower_coord.location.y, self.upper_coord.location.y])
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                coords.append(aoc.map.Coordinate(x,y))
        return coords
    
    def update_lower_z(self, z: int) -> None:
        if self.lower_coord.z == z:
            return
        if z > self.lower_coord.z:
            raise ValueError(f'{z} > {self.lower_coord}')
        delta_z = self.lower_coord.z - z
        self.lower_coord = self.lower_coord._replace(z=self.lower_coord.z - delta_z)
        self.upper_coord = self.upper_coord._replace(z=self.upper_coord.z - delta_z)

    def add_rests_on(self, other: 'Brick') -> None:
        log.log(log.INFO, f'Brick {self.num} rests on {other.num}')
        self.rests_on.add(other)

    def add_supports(self, other: 'Brick') -> None:
        log.log(log.INFO, f'Brick {self.num} supports {other.num}')
        self.supports.add(other)

    def can_be_disentegrated(self) -> bool:
        falling_bricks = self.would_fall()
        if falling_bricks:
            log.log(log.INFO, f'Brick {self.num} can\'t be disintegrated, {[brick.num for brick in falling_bricks]} rest on it')
            return False
        log.log(log.INFO, f'Brick {self.num} can be disintegrated')
        return True
    
    def would_fall(self) -> set['Brick']:
        return set(brick for brick in self.supports if len(brick.rests_on) == 1)
    
    def will_fall(self, removed: set['Brick']) -> bool:
        return len(self.rests_on - removed) == 0
    
    def __str__(self) -> str:
        return f'Brick({self.num}, {self.lower_coord}, {self.upper_coord}, {len(self.supports)}, {len(self.rests_on)})'


def settle(bricks: list[Brick]):
    max_z_occupied: dict[aoc.map.Coordinate, int] = collections.defaultdict(int)
    max_z_brick: dict[aoc.map.Coordinate, Brick] = {}
    for brick in sorted(bricks):
        log.log(log.DEBUG, f'Settling {brick}')
        coords = brick.coordinates()
        new_z = max(max_z_occupied[coord] for coord in coords) + 1
        
        rests_on: set[Brick] = set()
        for coord in coords:
            if new_z > 1 and max_z_occupied[coord] == new_z - 1:
                rests_on.add(max_z_brick[coord])

        brick.update_lower_z(new_z)
        for rests_on_brick in rests_on:
            brick.add_rests_on(rests_on_brick)
            rests_on_brick.add_supports(brick)

        max_z_occupied.update((coord, brick.upper_coord.z) for coord in coords)
        for coord in coords:
            max_z_brick.update((coord, brick) for coord in coords)
        log.log(log.DEBUG, f'Settled {brick}')
