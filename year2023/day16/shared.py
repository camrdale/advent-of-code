from abc import ABC, abstractmethod
from typing import NamedTuple

from aoc.input import InputParser
from aoc.map import ParsedMap, Coordinate, Offset, UP, RIGHT, DOWN, LEFT


class Beam(NamedTuple):
    location: Coordinate
    direction: Offset

    def next_beam(self):
        return self._replace(location=self.location.add(self.direction))


class BeamTransformer(ABC):
    @abstractmethod
    def transform(self, beam: Beam) -> tuple[Beam, ...]:
        pass


class MirrorUp(BeamTransformer):
    def transform(self, beam: Beam) -> tuple[Beam, ...]:
        if beam.direction == UP:
            return beam._replace(direction=RIGHT),
        if beam.direction == RIGHT:
            return beam._replace(direction=UP),
        if beam.direction == DOWN:
            return beam._replace(direction=LEFT),
        if beam.direction == LEFT:
            return beam._replace(direction=DOWN),
        return ()


class MirrorDown(BeamTransformer):
    def transform(self, beam: Beam) -> tuple[Beam, ...]:
        if beam.direction == UP:
            return beam._replace(direction=LEFT),
        if beam.direction == LEFT:
            return beam._replace(direction=UP),
        if beam.direction == DOWN:
            return beam._replace(direction=RIGHT),
        if beam.direction == RIGHT:
            return beam._replace(direction=DOWN),
        return ()


class Splitter(BeamTransformer):
    def __init__(self, *resulting_directions: Offset):
        self.resulting_directions = resulting_directions

    def transform(self, beam: Beam) -> tuple[Beam, ...]:
        if beam.direction not in self.resulting_directions:
            return tuple([beam._replace(direction=direction) for direction in self.resulting_directions])
        return beam,


OBJECTS: dict[str, BeamTransformer] = {
    '/': MirrorUp(),
    '\\': MirrorDown(),
    '|': Splitter(UP, DOWN),
    '-': Splitter(LEFT, RIGHT),
}


class BeamMap(ParsedMap):
    def __init__(self, parser: InputParser):
        super().__init__(parser.get_input(), ''.join(OBJECTS.keys()))

    def energize(self, starting_beam: Beam) -> set[Coordinate]:
        beams_to_process: list[Beam] = [starting_beam]
        found_beams: set[Beam] = set()
        energized_locations: set[Coordinate] = set()

        while len(beams_to_process) > 0:
            beam = beams_to_process.pop()
            if beam in found_beams:
                continue

            next_beam = beam.next_beam()
            for feature, transformer in OBJECTS.items():
                if next_beam.location in self.features[feature]:
                    beams_to_process.extend(transformer.transform(next_beam))
                    break
            else:
                if self.valid(next_beam.location):
                    beams_to_process.append(next_beam)

            found_beams.add(beam)
            energized_locations.add(beam.location)

        energized_locations.remove(starting_beam.location)
        return energized_locations
