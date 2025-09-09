from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day9.shared import GAME, play_game


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        game = GAME.match(input[0])
        assert game is not None
        num_players, num_points = map(int, game.groups())

        high_score = play_game(num_players, num_points)

        log.log(log.RESULT, f'The highest (winning) score: {high_score}')
        return high_score


part = Part1()

part.add_result(32, """
9 players; last marble is worth 25 points
""")

part.add_result(8317, """
10 players; last marble is worth 1618 points
""")

part.add_result(146373, """
13 players; last marble is worth 7999 points
""")

part.add_result(2764, """
17 players; last marble is worth 1104 points
""")

part.add_result(54718, """
21 players; last marble is worth 6111 points
""")

part.add_result(37305, """
30 players; last marble is worth 5807 points
""")

part.add_result(416424)
