from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day9.shared import GAME, play_game


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        game = GAME.match(input[0])
        assert game is not None
        num_players, num_points = map(int, game.groups())
        num_points *= 100

        high_score = play_game(num_players, num_points)

        log.log(log.RESULT, f'The highest (winning) score: {high_score}')
        return high_score


part = Part2()

part.add_result(3498287922)
