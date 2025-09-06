from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2018.day6.shared import Destination


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        total_distance_limit: int = parser.get_additional_params()[0]

        destinations = [Destination(line) for line in input]

        min_x = min(d.location.x for d in destinations)
        max_x = max(d.location.x for d in destinations)
        min_y = min(d.location.y for d in destinations)
        max_y = max(d.location.y for d in destinations)

        in_range_size = 0
        for y in range(min_y, max_y + 1):
            distances = sum(d.manhattan_distance(Coordinate(min_x, y)) for d in destinations)
            for x in range(min_x + 1, max_x + 1):
                distances += sum(-1 if x <= d.location.x else 1 for d in destinations)
                if distances < total_distance_limit:
                    in_range_size += 1

        log.log(log.RESULT, f'The size of the region which is less than {total_distance_limit} from all destinations: {in_range_size}')
        return in_range_size


part = Part2()

part.add_result(16, """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""", 32)

part.add_result(43302, None, 10000)
