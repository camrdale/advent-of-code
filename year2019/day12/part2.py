import itertools
import math
import re

import aoc.input
from aoc import log
from aoc import runner

COORDS = re.compile(r'<x=([0-9-]*), y=([0-9-]*), z=([0-9-]*)>')


def cmp(a: int, b: int) -> int:
    if a < b:
        return 1
    elif a > b:
        return -1
    return 0


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_parsed_int_input(COORDS)

        moon_positions: list[list[int]] = []
        for x, y, z in input:
            moon_positions.append([x,y,z])

        moon_velocities = [[0,0,0] for _ in range(len(moon_positions))]

        repeated_steps: list[int] = []
        for coord in range(3):
            found_states: dict[tuple[int, ...], int] = {}
            step = 0
            while True:
                state = tuple([position[coord] for position in moon_positions] + [velocity[coord] for velocity in moon_velocities])
                if state in found_states:
                    log.log(log.INFO, f'The {coord} state repeated step {found_states[state]} after {step} steps: {state}')
                    repeated_steps.append(step)
                    break
                found_states[state] = step
                for moon1, moon2 in itertools.combinations(range(len(moon_positions)), 2):
                    dv = cmp(moon_positions[moon1][coord], moon_positions[moon2][coord])
                    moon_velocities[moon1][coord] += dv
                    moon_velocities[moon2][coord] += -dv
                for position, velocity in zip(moon_positions, moon_velocities):
                    position[coord] += velocity[coord]
                step += 1

        repeat_steps = math.lcm(*repeated_steps)
        log.log(log.RESULT, f'The system repeates after: {repeat_steps}')
        return repeat_steps


part = Part2()

part.add_result(2772, r"""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""")

part.add_result(4686774924, r"""
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""")

part.add_result(543673227860472)
