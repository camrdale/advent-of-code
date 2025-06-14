from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day14.shared import Reindeer


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        race_time: int = parser.get_additional_params()[0]

        farthest_distance = 0
        for line in input:
            reindeer = Reindeer.from_text(line)
            distance = reindeer.distance(race_time)

            log.log(log.INFO, f'{reindeer.name} travels {distance} km')
            if distance > farthest_distance:
                farthest_distance = distance

        log.log(log.RESULT, f'The winning reindeer travels a distance of: {farthest_distance} km')
        return farthest_distance


part = Part1()

part.add_result(1120, """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
""", 1000)

part.add_result(2660, None, 2503)
