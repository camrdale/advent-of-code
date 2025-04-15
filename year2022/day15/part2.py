from collections import defaultdict
import itertools
import re
from typing import NamedTuple

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part


SENSOR = re.compile(r'Sensor at x=([0-9-]*), y=([0-9-]*): closest beacon is at x=([0-9-]*), y=([0-9-]*)')


class LineSegment(NamedTuple):
    location: Coordinate  # left-most location on line (smallest x value)
    slope: int  # 1 or -1
    length: int  # manhattan length

    def b(self) -> int:
        return self.location.y - (self.slope * self.location.x)

    def intersection(self, other: 'LineSegment') -> Coordinate | None:
        if self.slope == other.slope:
            return None
        b1 = self.b() if self.slope == 1 else other.b()
        b2 = self.b() if self.slope == -1 else other.b()
        if (b2 - b1) % 2 == 1:
            # Ignore non-integer intersections
            return None
        intersect_x = (b2 - b1) // 2
        if self.location.x <= intersect_x <= self.location.x + self.length and other.location.x <= intersect_x <= other.location.x + other.length:
            log.log(log.DEBUG, f'Found intersection at {intersect_x} for lines: {self}, {other}')
            return Coordinate(intersect_x, self.slope * intersect_x + self.b())
        return None


def detected(location: Coordinate, sensors: list[tuple[Coordinate, int]]) -> bool:
    for sensor, sensor_range in sensors:
        if sensor.difference(location).manhattan_distance() <= sensor_range:
            return True
    return False


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_parsed_input(SENSOR)
        max_coordinate: int = parser.get_additional_params()[0]

        boundary_lines: list[LineSegment] = []
        sensors: list[tuple[Coordinate, int]] = []
        for sensor_input in input:
            sensor = Coordinate(int(sensor_input[0]), int(sensor_input[1]))
            beacon = Coordinate(int(sensor_input[2]), int(sensor_input[3]))
            sensor_range = beacon.difference(sensor).manhattan_distance()
            sensors.append((sensor, sensor_range))

            # 4 line segments that are the boundaries of (one outside) the detection ranges of this sensor
            boundary_lines.append(LineSegment(Coordinate(sensor.x - sensor_range - 1, sensor.y), 1, sensor_range + 1))
            boundary_lines.append(LineSegment(Coordinate(sensor.x - sensor_range - 1, sensor.y), -1, sensor_range + 1))
            boundary_lines.append(LineSegment(Coordinate(sensor.x, sensor.y - sensor_range - 1), 1, sensor_range + 1))
            boundary_lines.append(LineSegment(Coordinate(sensor.x, sensor.y + sensor_range + 1), -1, sensor_range + 1))

        # A single undetected point must be at the intersection of at least 4 boundary line segments
        intersection_points: dict[Coordinate, int] = defaultdict(int)
        for line1, line2 in itertools.combinations(boundary_lines, 2):
            intersection = line1.intersection(line2)
            if intersection is not None:
                intersection_points[intersection] += 1
        busiest_intersections = sorted([(num_intersections, location) for location, num_intersections in intersection_points.items()], reverse=True)
        log.log(log.DEBUG, f'Found {len(busiest_intersections)} interesting points: {busiest_intersections}')

        for num_intersections, location in busiest_intersections:
            if location.x < 0 or location.x > max_coordinate or location.y < 0 or location.y > max_coordinate:
                log.log(log.INFO, f'Ignoring out of range busy intersection with {num_intersections} intersections: {location}')
                continue
            if detected(location, sensors):
                log.log(log.INFO, f'Ignoring detected busy intersection with {num_intersections} intersections: {location}')
                continue

            log.log(log.RESULT, f'The beacon could be at {location} with tuning frequency: {location.x*4000000 + location.y}')
            return location.x*4000000 + location.y
        
        raise ValueError(f'Failed to find an undetected sensor location')


part = Part2()

part.add_result(56000011, r"""
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""", 20)

part.add_result(11756174628223, None, 4000000)
