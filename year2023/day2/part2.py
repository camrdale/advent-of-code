import math

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


def game_power(record: str) -> int:
    min_cubes: dict[str, int] = {}
    revealed = record.split(';')
    for reveal in revealed:
        cubes = reveal.strip().split(',')
        for cube in cubes:
            cube_num, cube_color = cube.split()
            if cube_color in min_cubes:
                min_cubes[cube_color] = max(int(cube_num), min_cubes[cube_color])
            else:
                min_cubes[cube_color] = int(cube_num)
    return math.prod(min_cubes.values())


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_game_powers = 0
        for line in input:
            _, record = line.split(':')
            sum_game_powers += game_power(record)

        log(RESULT, f'The sum of the power of the games: {sum_game_powers}')
        return sum_game_powers


part = Part2()

part.add_result(2286, """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""")

part.add_result(2265)
