import re

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.range import Range
from aoc.runner import Part


SENSOR = re.compile(r'Sensor at x=([0-9-]*), y=([0-9-]*): closest beacon is at x=([0-9-]*), y=([0-9-]*)')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_parsed_input(SENSOR)
        row: int = parser.get_additional_params()[0]

        beacons_in_row: set[int] = set()
        ranges: list[Range] = []
        for sensor_input in input:
            sensor = Coordinate(int(sensor_input[0]), int(sensor_input[1]))
            beacon = Coordinate(int(sensor_input[2]), int(sensor_input[3]))
            if beacon.y == row:
                beacons_in_row.add(beacon.x)
            sensor_range = beacon.difference(sensor).manhattan_distance()
            range_in_row = sensor_range - abs(sensor.y - row)
            if range_in_row >= 0:
                ranges.append(Range.closed(sensor.x - range_in_row, sensor.x + range_in_row))

        ranges.sort(reverse=True)
        log.log(log.DEBUG, ranges)

        merged_ranges = [ranges.pop()]
        while ranges:
            next_range = ranges.pop()
            merged_range = merged_ranges[-1].merge(next_range)
            if merged_range is None:
                merged_ranges.append(next_range)
            else:
                merged_ranges[-1] = merged_range

        log.log(log.DEBUG, merged_ranges)
        positions_with_no_beacon = sum(range.length() for range in merged_ranges) - len(beacons_in_row)
        log.log(log.RESULT, f'In row {row}, the number of positions that cannot contain a beacon: {positions_with_no_beacon}')
        return positions_with_no_beacon


part = Part1()

part.add_result(26, r"""
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
""", 10)

part.add_result(5525990, None, 2000000)
