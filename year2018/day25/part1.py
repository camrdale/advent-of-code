from typing import NamedTuple

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Coordinate3D, Offset3D, Offset
from aoc.runner import Part
from aoc.sets import DisjointSet


class Offset4D(NamedTuple):
    offset: Offset3D
    t: int

    def manhattan_distance(self) -> int:
        return self.offset.manhattan_distance() + abs(self.t)


class Coordinate4D(NamedTuple):
    location: Coordinate3D
    t: int

    @classmethod
    def from_text(cls, text: str) -> Coordinate4D:
        x,y,z, t = list(map(int, text.split(',')))
        return cls(Coordinate3D(z, Coordinate(x,y)), t)

    def difference(self, from_coordinate: Coordinate4D) -> Offset4D:
        return Offset4D(self.location.difference(from_coordinate.location), self.t - from_coordinate.t)
    
    def add(self, offset: Offset4D) -> Coordinate4D:
        return Coordinate4D(self.location.add(offset.offset), self.t + offset.t)


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        # Build a list of all (128) offsets that are <= 3 distance.
        # Checking if 128 values are in the sets is 5X faster than checking the
        # distance of each (1047) point from each existing point in the sets.
        distance_3: list[Offset4D] = []
        remaining = 3
        for x in range(-remaining, remaining + 1):
            remaining = 3 - abs(x)
            for y in range(-remaining, remaining + 1):
                remaining = 3 - abs(x) - abs(y)
                for z in range(-remaining, remaining + 1):
                    remaining = 3 - abs(x) - abs(y) - abs(z)
                    for t in range(-remaining, remaining + 1):
                        distance_3.append(Offset4D(Offset3D(z, Offset(x,y)), t))
        distance_3.remove(Offset4D(Offset3D(0, Offset(0,0)), 0))

        disjoint_set: DisjointSet[Coordinate4D] = DisjointSet()
        for line in input:
            point = Coordinate4D.from_text(line)
            disjoint_set.add(point)
            for offset in distance_3:
                # Check each location that could be in range of this one, to see if it exists.
                node = point.add(offset)
                if node in disjoint_set.nodes:
                    disjoint_set.union(node, point)

        num_constellations = disjoint_set.size()

        log.log(log.RESULT, f'The number of constellations in the points: {num_constellations}')
        return num_constellations


part = Part1()

part.add_result(2, """
0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0
""")

part.add_result(4, """
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
""")

part.add_result(3, """
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
""")

part.add_result(8, """
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
""")

part.add_result(430)
