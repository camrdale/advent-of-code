import itertools
import re

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

COORDS = re.compile(r'<x=([0-9-]*), y=([0-9-]*), z=([0-9-]*)>')


def cmp(a: int, b: int) -> int:
    if a < b:
        return 1
    elif a > b:
        return -1
    return 0


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_parsed_input(COORDS)
        steps: int = parser.get_additional_params()[0]

        moon_positions: list[list[int]] = []
        for line in input:
            x, y, z = map(int, line)
            moon_positions.append([x,y,z])

        moon_velocities = [[0,0,0] for _ in range(len(moon_positions))]

        for step in range(steps):
            log.log(log.INFO, f'After {step} steps:')
            for position, velocity in zip(moon_positions, moon_velocities):
                log.log(log.INFO, f'pos=<x={position[0]}, y={position[1]}, z={position[2]}>, vel=<x={velocity[0]}, y={velocity[1]}, z={velocity[2]}>')
            log.log(log.INFO, '')
            for moon1, moon2 in itertools.combinations(range(len(moon_positions)), 2):
                for coord in range(3):
                    dv = cmp(moon_positions[moon1][coord], moon_positions[moon2][coord])
                    moon_velocities[moon1][coord] += dv
                    moon_velocities[moon2][coord] += -dv
            for position, velocity in zip(moon_positions, moon_velocities):
                for coord in range(3):
                    position[coord] += velocity[coord]

        log.log(log.INFO, f'After {steps} steps:')
        for position, velocity in zip(moon_positions, moon_velocities):
            log.log(log.INFO, f'pos=<x={position[0]}, y={position[1]}, z={position[2]}>, vel=<x={velocity[0]}, y={velocity[1]}, z={velocity[2]}>')

        total_energy = 0
        for position, velocity in zip(moon_positions, moon_velocities):
            total_energy += sum(map(abs, position)) * sum(map(abs, velocity))

        log.log(log.RESULT, f'Sum of total energy in the system: {total_energy}')
        return total_energy


part = Part1()

part.add_result(179, r"""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""", 10)

part.add_result(1940, r"""
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""", 100)

part.add_result(14606, None, 1000)
