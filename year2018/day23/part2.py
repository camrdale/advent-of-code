from collections.abc import Iterable
import heapq
from typing import NamedTuple, Self

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate3D, Coordinate
from aoc.range import Range
from aoc.runner import Part

from year2018.day23.shared import Nanobot


ORIGIN = Coordinate3D(0, Coordinate(0, 0))


class Cube(NamedTuple):
    x: Range
    y: Range
    z: Range

    def nanobots_in_range(self, nanobots: Iterable[Nanobot]) -> tuple[Nanobot, ...]:
        """Return a tuple of the nanobots whose range touch this cube."""
        return tuple(nanobot for nanobot in nanobots if self.in_range(nanobot))

    def in_range(self, nanobot: Nanobot) -> bool:
        """Determine if the nanobot's range touches this cube."""
        closest_x = self.x.closest_to(nanobot.location.location.x)
        closest_y = self.y.closest_to(nanobot.location.location.y)
        closest_z = self.z.closest_to(nanobot.location.z)
        return nanobot.in_range(Coordinate3D(closest_z, Coordinate(closest_x, closest_y)))

    def divide(self) -> list[Cube]:
        """Divide the cube into smaller pieces, if possible."""
        result: list[Cube] = []
        for x_range in self.x.split():
            if x_range is None:
                continue
            for y_range in self.y.split():
                if y_range is None:
                    continue
                for z_range in self.z.split():
                    if z_range is None:
                        continue
                    result.append(Cube(x_range, y_range, z_range))
        return result

    def size(self) -> int:
        return self.x.length() * self.y.length() * self.z.length()

    def distance_from_origin(self) -> int:
        return Coordinate3D(
            self.z.closest_to(0),
            Coordinate(self.x.closest_to(0),
                       self.y.closest_to(0))
            ).difference(ORIGIN).manhattan_distance()


class CubeStats(NamedTuple):
    # Prioritize based on most nanobots in range, closest to origin, and smallest cube.
    neg_nanobots_in_range: int
    distance: int
    size: int
    cube: Cube
    nanobots_in_range: tuple[Nanobot, ...]

    @classmethod
    def from_cube(cls, cube: Cube, nanobots: Iterable[Nanobot]) -> Self:
        in_range = cube.nanobots_in_range(nanobots)
        return cls(-len(in_range), cube.distance_from_origin(), cube.size(), cube, in_range)

    @classmethod
    def best(cls, nanobots: list[Nanobot]) -> CubeStats:
        # Create a cube that contains all of the nanobots and their ranges.
        cube = Cube(
            Range.closed(min(nanobot.location.location.x - nanobot.radius for nanobot in nanobots),
                         max(nanobot.location.location.x + nanobot.radius for nanobot in nanobots)),
            Range.closed(min(nanobot.location.location.y - nanobot.radius for nanobot in nanobots),
                         max(nanobot.location.location.y + nanobot.radius for nanobot in nanobots)),
            Range.closed(min(nanobot.location.z - nanobot.radius for nanobot in nanobots),
                         max(nanobot.location.z + nanobot.radius for nanobot in nanobots)))

        # Priority queue of the cubes with the most nanobots in their range.
        cubes_to_try: list[CubeStats] = []
        heapq.heappush(cubes_to_try, CubeStats.from_cube(cube, nanobots))

        while cubes_to_try:
            cube_stats = heapq.heappop(cubes_to_try)

            divided = cube_stats.cube.divide()
            if len(divided) == 1:
                # The cube can't be divided any more. The first one will always be the answer.
                return cube_stats

            for cube in divided:
                # Add each piece of the cube to priority queue to try.
                heapq.heappush(cubes_to_try, CubeStats.from_cube(cube, cube_stats.nanobots_in_range))

        raise ValueError(f'Failed to find the best cube.')


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        nanobots: list[Nanobot] = []
        for line in input:
            nanobots.append(Nanobot.from_text(line))

        cube_stats = CubeStats.best(nanobots)

        log.log(log.RESULT, f'The location in range of {-cube_stats.neg_nanobots_in_range} nanobots: {cube_stats.cube}')
        return cube_stats.distance


part = Part2()

part.add_result(36, """
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
""")

part.add_result(82010396)
