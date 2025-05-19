from collections import defaultdict, Counter
from collections.abc import Callable
import enum
import itertools
import operator
import re
from typing import NamedTuple, Any

from aoc import log
from aoc.map import Coordinate3D, Coordinate, Offset3D


SCANNER = re.compile(r'--- scanner ([0-9]*) ---')


class Orientator:
    def __init__(self, orientation_function: Callable[[Coordinate3D], Coordinate3D]) -> None:
        self.orientation_function = orientation_function
    
    def orient(self, location: Coordinate3D) -> Coordinate3D:
        return self.orientation_function(location)


class Orientation(enum.Enum):
    FACING_X_Z_UP = Orientator(lambda c: Coordinate3D(c.z, Coordinate(c.location.x, c.location.y)))
    FACING_X_Z_DOWN = Orientator(lambda c: Coordinate3D(-c.z, Coordinate(c.location.x, -c.location.y)))
    FACING_NEG_X_Z_UP = Orientator(lambda c: Coordinate3D(c.z, Coordinate(-c.location.x, -c.location.y)))
    FACING_NEG_X_Z_DOWN = Orientator(lambda c: Coordinate3D(-c.z, Coordinate(-c.location.x, c.location.y)))
    FACING_Y_Z_UP = Orientator(lambda c: Coordinate3D(c.z, Coordinate(-c.location.y, c.location.x)))
    FACING_Y_Z_DOWN = Orientator(lambda c: Coordinate3D(-c.z, Coordinate(c.location.y, c.location.x)))
    FACING_NEG_Y_Z_UP = Orientator(lambda c: Coordinate3D(c.z, Coordinate(c.location.y, -c.location.x)))
    FACING_NEG_Y_Z_DOWN = Orientator(lambda c: Coordinate3D(-c.z, Coordinate(-c.location.y, -c.location.x)))
    FACING_X_Y_UP = Orientator(lambda c: Coordinate3D(-c.location.y, Coordinate(c.location.x, c.z)))
    FACING_X_Y_DOWN = Orientator(lambda c: Coordinate3D(c.location.y, Coordinate(c.location.x, -c.z)))
    FACING_NEG_X_Y_UP = Orientator(lambda c: Coordinate3D(c.location.y, Coordinate(-c.location.x, c.z)))
    FACING_NEG_X_Y_DOWN = Orientator(lambda c: Coordinate3D(-c.location.y, Coordinate(-c.location.x, -c.z)))
    FACING_Z_Y_UP = Orientator(lambda c: Coordinate3D(c.location.x, Coordinate(c.location.y, c.z)))
    FACING_Z_Y_DOWN = Orientator(lambda c: Coordinate3D(c.location.x, Coordinate(-c.location.y, -c.z)))
    FACING_NEG_Z_Y_UP = Orientator(lambda c: Coordinate3D(-c.location.x, Coordinate(-c.location.y, c.z)))
    FACING_NEG_Z_Y_DOWN = Orientator(lambda c: Coordinate3D(-c.location.x, Coordinate(c.location.y, -c.z)))
    FACING_Y_X_UP = Orientator(lambda c: Coordinate3D(c.location.y, Coordinate(c.z, c.location.x)))
    FACING_Y_X_DOWN = Orientator(lambda c: Coordinate3D(-c.location.y, Coordinate(-c.z, c.location.x)))
    FACING_NEG_Y_X_UP = Orientator(lambda c: Coordinate3D(-c.location.y, Coordinate(c.z, -c.location.x)))
    FACING_NEG_Y_X_DOWN = Orientator(lambda c: Coordinate3D(c.location.y, Coordinate(-c.z, -c.location.x)))
    FACING_Z_X_UP = Orientator(lambda c: Coordinate3D(c.location.x, Coordinate(c.z, -c.location.y)))
    FACING_Z_X_DOWN = Orientator(lambda c: Coordinate3D(c.location.x, Coordinate(-c.z, c.location.y)))
    FACING_NEG_Z_X_UP = Orientator(lambda c: Coordinate3D(-c.location.x, Coordinate(c.z, c.location.y)))
    FACING_NEG_Z_X_DOWN = Orientator(lambda c: Coordinate3D(-c.location.x, Coordinate(-c.z, -c.location.y)))


class Translator(NamedTuple):
    offset: Offset3D
    orientation: Orientation

    def translate(self, location: Coordinate3D) -> Coordinate3D:
        return self.orientation.value.orient(location).add(self.offset)

    @classmethod
    def find_orientations(
            cls,
            scanner_a_beacons: tuple[Coordinate3D, Coordinate3D],
            scanner_b_beacons: tuple[Coordinate3D, Coordinate3D],
            flip: bool = False
            ) -> list['Translator']:
        possibilities: list[Translator] = []
        for orientation in Orientation:
            oriented_b_beacon_0 = orientation.value.orient(scanner_b_beacons[0])
            offset = scanner_a_beacons[0].difference(oriented_b_beacon_0)
            possibility = cls(offset, orientation)
            if possibility.translate(scanner_b_beacons[0]) != scanner_a_beacons[0]:
                raise ValueError(f'Expected translation {possibility} to translate {scanner_b_beacons[0]} to {scanner_a_beacons[0]}, got {possibility.translate(scanner_b_beacons[0])}')
            if possibility.translate(scanner_b_beacons[1]) == scanner_a_beacons[1]:
                possibilities.append(possibility)
        if not flip:
            possibilities.extend(cls.find_orientations(scanner_a_beacons, (scanner_b_beacons[1], scanner_b_beacons[0]), flip=True))
        return possibilities


class Scanner:
    def __init__(self, input: list[str]):
        match = SCANNER.match(input[0])
        assert match is not None, input[0]
        self.num = int(match.group(1))

        self.beacons: set[Coordinate3D] = set()
        for line in input[1:]:
            beacon = Coordinate3D.from_text(line)
            self.beacons.add(beacon)

        self.beacon_distances: dict[int, list[tuple[Coordinate3D, Coordinate3D]]] = defaultdict(list)
        for beacon_a, beacon_b in itertools.combinations(self.beacons, 2):
            self.beacon_distances[beacon_a.difference(beacon_b).manhattan_distance()].append((beacon_a, beacon_b))

        distance_counts = Counter(map(len, self.beacon_distances.values()))
        log.log(log.DEBUG, f'Scanner {self.num} has beacon distance distribution: {distance_counts}')

    def add_beacons(self, beacons: set[Coordinate3D]):
        for new_beacon in beacons:
            if new_beacon in self.beacons:
                continue
            for beacon in self.beacons:
                self.beacon_distances[beacon.difference(new_beacon).manhattan_distance()].append((beacon, new_beacon))
            self.beacons.add(new_beacon)

        distance_counts = Counter(map(len, self.beacon_distances.values()))
        log.log(log.INFO, f'Scanner {self.num} now has beacon distance distribution: {distance_counts}')

    def find_overlap(self, scanners: set['Scanner']) -> tuple['Scanner', Translator]:
        best_scanners: list[tuple[int, Scanner]] = []
        for scanner in scanners:
            common_distances = self.beacon_distances.keys() & scanner.beacon_distances.keys()
            log.log(log.DEBUG, f'Scanner {scanner.num} has {len(common_distances)} beacon distances in common with this Scanner')
            best_scanners.append((len(common_distances), scanner))
        
        best_scanners.sort(reverse=True, key=operator.itemgetter(0))
        for num_common_distances, scanner in best_scanners:
            log.log(log.INFO, f'Trying Scanner {scanner.num} which has {num_common_distances} beacon distances in common with this Scanner')
            common_distances = self.beacon_distances.keys() & scanner.beacon_distances.keys()
            for distance in common_distances:
                if len(self.beacon_distances[distance]) > 1:
                    log.log(log.DEBUG, f'Too many this scanner distances of {distance}: {self.beacon_distances[distance]}')
                    continue
                if len(scanner.beacon_distances[distance]) > 1:
                    log.log(log.DEBUG, f'Too many best scanner distances of {distance}: {scanner.beacon_distances[distance]}')
                    continue
                self_beacons = next(iter(self.beacon_distances[distance]))
                scanner_beacons = next(iter(scanner.beacon_distances[distance]))
                for translator in Translator.find_orientations(self_beacons, scanner_beacons):
                    translated_beacons = set(translator.translate(beacon) for beacon in scanner.beacons)
                    if len(self.beacons & translated_beacons) >= 12:
                        log.log(log.INFO, f'{translator} Found {len(self.beacons & translated_beacons)} overlapping beacons: {self.beacons & translated_beacons}')
                        return scanner, translator
                    log.log(log.INFO, f'Too few translated beacons overlap for {translator}: {self.beacons & translated_beacons}')
        raise ValueError(f'Failed to find overlap between this scanners beacons and {scanners}')

    def __eq__(self, other: Any) -> bool:
        if type(other) != Scanner:
            return False
        return self.num == other.num

    def __hash__(self) -> int:
        return hash(self.num)
    
    def __repr__(self) -> str:
        return f'Scanner-{self.num}'
