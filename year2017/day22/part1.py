from aoc.input import InputParser
from aoc import log
from aoc.map import ParsedMap, Coordinate, Direction
from aoc.runner import Part


VIRUS = '#'


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        virus_map = ParsedMap(input, VIRUS)

        location = Coordinate(virus_map.max_x // 2, virus_map.max_y // 2)
        direction = Direction.NORTH
        infections_caused = 0
        for burst in range(10_000):
            if burst in (0, 7, 70):
                log.log(log.INFO, f'After {burst:,} bursts, there have been {infections_caused} infections caused')
                log.log(log.DEBUG, virus_map.print_map)
            if location in virus_map.features[VIRUS]:
                direction = direction.right()
                virus_map.features[VIRUS].remove(location)
            else:
                direction = direction.left()
                virus_map.add_feature(VIRUS, location)
                infections_caused += 1
            location = location.add(direction.offset())

        log.log(log.DEBUG, virus_map.print_map)

        log.log(log.RESULT, f'After 10,000 bursts, the number of infections caused: {infections_caused}')
        return infections_caused


part = Part1()

part.add_result(5587, """
..#
#..
...
""")

part.add_result(5259)
