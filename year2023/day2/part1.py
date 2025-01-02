from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

MAX_CUBES = {'red': 12, 'green': 13, 'blue': 14}


def possible(record: str) -> bool:
    revealed = record.split(';')
    for reveal in revealed:
        cubes = reveal.strip().split(',')
        for cube in cubes:
            cube_num, cube_color = cube.split()
            if int(cube_num) > MAX_CUBES[cube_color]:
                return False
    return True


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_possible_games = 0
        for line in input:
            game, record = line.split(':')
            game_id = int(game.split()[1])
            if possible(record):
                sum_possible_games += game_id

        log(RESULT, f'The sum of all possible games: {sum_possible_games}')
        return sum_possible_games


part = Part1()

part.add_result(8, """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""")

part.add_result(2265)
