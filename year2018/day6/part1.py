from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2018.day6.shared import Destination


def populate_closest_area(destinations: list[Destination]) -> None:
    min_x = min(d.location.x for d in destinations)
    max_x = max(d.location.x for d in destinations)
    min_y = min(d.location.y for d in destinations)
    max_y = max(d.location.y for d in destinations)
    
    for y in range(min_y, max_y + 1):
        location = Coordinate(min_x, y)
        distances = [
            (d.manhattan_distance(location), d)
            for d in destinations]
        distances.sort()

        if distances[0][0] != distances[1][0]:
            destination = distances[0][1]
            destination.closest_area.add(location)
            destination.infinite = True

        for x in range(min_x + 1, max_x + 1):
            location = Coordinate(x, y)
            distances = [
                (old_distance + (-1 if x <= destination.location.x else 1), destination)
                for (old_distance, destination) in distances]
            distances.sort()

            if distances[0][0] == distances[1][0]:
                continue
            destination = distances[0][1]
            destination.closest_area.add(location)
            if x == min_x or x == max_x or y == min_y or y == max_y:
                destination.infinite = True


def largest_noninfinite_area_key(destination: Destination) -> int:
    return len(destination.closest_area) * (-1 if destination.infinite else 1)


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        destinations = [Destination(line) for line in input]

        populate_closest_area(destinations)

        largest_area_destination = max(destinations, key=largest_noninfinite_area_key)

        log.log(log.RESULT, f'The largest area is around {largest_area_destination.location}: {len(largest_area_destination.closest_area)}')
        return len(largest_area_destination.closest_area)


part = Part1()

part.add_result(17, """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""")

part.add_result(2342)
