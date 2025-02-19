from aoc.input import InputParser
from aoc import log
from aoc.map import EmptyMap, Coordinate
from aoc.runner import Part

from year2019.day19 import shared


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        drone = shared.DroneProgram(intcode_input)

        scan = EmptyMap(0, 0, 49, 49)
        scan.save_features += '#'
        moving = 0

        # Beam is irregular for small y, just iterate these ones
        for y in range(5):
            for x in range(0, 10):
                location = Coordinate(x,y)
                if drone.is_moving(location):
                    moving += 1
                    scan.features['#'].add(location)

        for y in range(5, 50):
            start, end = drone.get_beam(y)
            for x in range(start.x, end.x + 1):
                location = Coordinate(x,y)
                moving += 1
                scan.features['#'].add(location)
                
        log.log(log.INFO, scan.print_map())
        log.log(log.RESULT, f'The number of points affected by the tractor beam: {moving}')
        return moving


part = Part1()

part.add_result(186)
