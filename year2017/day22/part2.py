from aoc.input import InputParser
from aoc import log
from aoc.map import ParsedMap, Coordinate, Direction
from aoc.runner import Part


VIRUS = '#'
WEAKENED = 'W'
FLAGGED = 'F'


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        virus_map = ParsedMap(input, VIRUS + WEAKENED + FLAGGED)

        location = Coordinate(virus_map.max_x // 2, virus_map.max_y // 2)
        direction = Direction.NORTH
        infections_caused = 0
        for burst in log.progress_bar(range(10_000_000), desc='day 22,2'):
            if burst in (0, 7, 100) or burst % 1_000_000 == 0:
                log.log(log.INFO, f'After {burst:,} bursts, there have been {infections_caused} infections caused')
                log.log(log.DEBUG, virus_map.print_map)

            if location in virus_map.features[VIRUS]:
                direction = direction.right()
                virus_map.features[VIRUS].remove(location)
                virus_map.features[FLAGGED].add(location)
            elif location in virus_map.features[FLAGGED]:
                direction = direction.right().right()
                virus_map.features[FLAGGED].remove(location)
            elif location in virus_map.features[WEAKENED]:
                virus_map.features[WEAKENED].remove(location)
                virus_map.features[VIRUS].add(location)
                infections_caused += 1
            else:
                direction = direction.left()
                virus_map.add_feature(WEAKENED, location)

            location = location.add(direction.offset())

        log.log(log.DEBUG, virus_map.print_map)

        log.log(log.RESULT, f'After 10,000,000 bursts, the number of infections caused: {infections_caused}')
        return infections_caused


part = Part2()

# Too slow
# part.add_result(2511944, """
# ..#
# #..
# ...
# """)

part.add_result(2511722)
