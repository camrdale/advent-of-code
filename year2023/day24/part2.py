import itertools

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2023.day24 import shared


def all_intersect(hailstones: list[shared.Hailstone]) -> bool:
    for hail1, hail2 in itertools.combinations(hailstones, 2):
        if not hail1.intersect(hail2, 0, 128127524808597400):
            return False
    return True


def find_all_intersect_offset(hailstones: list[shared.Hailstone]) -> aoc.map.Offset:
    tried: set[tuple[int, ...]] = set()
    i = 0
    for num1 in range(1000):
        for num2 in range(num1+1):
            for v in itertools.permutations([-num1, -num2, num1, num2], 2):
                    if v not in tried:
                        tried.add(v)
                        i += 1
                        offset = aoc.map.Offset(v[0], v[1])
                        relative_hailstones = [hailstone._replace(velocity=aoc.map.Offset3D(hailstone.velocity.z, hailstone.velocity.offset.add(offset))) for hailstone in hailstones]
                        if all_intersect(relative_hailstones):
                            return offset.negate()
    raise ValueError(f'Failed to find all intersect after {i} iterations')


def find_all_intersect_velocity(hailstones: list[shared.Hailstone]) -> aoc.map.Offset3D:
    xy_offset = find_all_intersect_offset(hailstones)
    use_z_for_y = [shared.Hailstone(
        hailstone.position._replace(location=hailstone.position.location._replace(y=hailstone.position.z)),
        hailstone.velocity._replace(offset=hailstone.velocity.offset._replace(y=hailstone.velocity.z))) for hailstone in hailstones]
    for z in range(1000):
        for sign in (1, -1):
            offset = aoc.map.Offset(-xy_offset.x, z*sign)
            relative_hailstones = [hailstone._replace(velocity=aoc.map.Offset3D(hailstone.velocity.z, hailstone.velocity.offset.add(offset))) for hailstone in use_z_for_y]
            if all_intersect(relative_hailstones):
                return aoc.map.Offset3D(-z*sign, xy_offset)
    raise ValueError(f'Failed to find all intersect after {1000} iterations')


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        hailstones: list[shared.Hailstone] = []
        for line in input:
            hailstones.append(shared.Hailstone.from_text(line))

        offset = find_all_intersect_velocity(hailstones)
        log.log(log.DEBUG, f'All hailstones intersect with a line with velocity: {offset}')

        vx = offset.offset.x
        vy = offset.offset.y
        x1 = hailstones[0].position.location.x
        x2 = hailstones[1].position.location.x
        y1 = hailstones[0].position.location.y
        y2 = hailstones[1].position.location.y
        vx1 = hailstones[0].velocity.offset.x
        vx2 = hailstones[1].velocity.offset.x
        vy1 = hailstones[0].velocity.offset.y
        vy2 = hailstones[1].velocity.offset.y

        t2 = ((y2-y1)*(vx1-vx) - (x2-x1)*(vy1-vy)) / ((vx2-vx)*(vy1-vy) - (vy2-vy)*(vx1-vx))
        x = x2 + t2*vx2 - t2*vx
        y = y2 + t2*vy2 - t2*vy
        z = hailstones[1].position.z + t2*hailstones[1].velocity.z - t2*offset.z
        rock_frame_of_reference = aoc.map.Offset3D(-round(z), aoc.map.Offset(-round(x), -round(y)))
        log.log(log.DEBUG, f'The initial position of the rock is: {y}, {y}, {z}')

        for hailstone in hailstones:
            relative_v = hailstone.velocity.add(offset.negate())
            relative_position = hailstone.position.add(rock_frame_of_reference)
            intersect_at = - relative_position.location.x / relative_v.offset.x
            y_at_intersection = relative_position.location.y + intersect_at * relative_v.offset.y
            z_at_intersection = relative_position.z + intersect_at * relative_v.z
            log.log(log.INFO, f'Hailstone: {hailstone}')
            log.log(log.INFO, f'Collision time: {intersect_at} (relative y={y_at_intersection},z={z_at_intersection})')
            x1 = hailstone.position.location.x + intersect_at * hailstone.velocity.offset.x
            y1 = hailstone.position.location.y + intersect_at * hailstone.velocity.offset.y
            z1 = hailstone.position.z + intersect_at * hailstone.velocity.z
            log.log(log.INFO, f'Collision position: {x1} {y1} {z1}\n')
        
        log.log(log.RESULT, f'The initial position x,y,z coords sum to: {x + y + z}')
        return round(x + y + z)


part = Part2()

part.add_result(47, r"""
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""")

part.add_result(757031940316991)
