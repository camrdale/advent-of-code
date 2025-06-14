import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day14.shared import Reindeer


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        race_time: int = parser.get_additional_params()[0]

        reindeers: list[Reindeer] = []
        for line in input:
            reindeers.append(Reindeer.from_text(line))

        points: dict[str, int] = collections.defaultdict(int)
        for time in range(1, race_time + 1):
            current_positions = [
                (reindeer.distance(time), reindeer)
                for reindeer in reindeers]
            current_positions.sort(reverse=True)
            lead = current_positions[0][0]
            for distance, reindeer in current_positions:
                if distance == lead:
                    points[reindeer.name] += 1
                else:
                    break
        
        log.log(log.INFO, f'Points at the end of the race: {points}')

        max_points = max(points.values())

        log.log(log.RESULT, f'The winning reindeer has: {max_points} points')
        return max_points


part = Part2()

part.add_result(689, """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
""", 1000)

part.add_result(1256, None, 2503)
