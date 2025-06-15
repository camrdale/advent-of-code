from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day15.shared import CookieOptimizer


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        optimizer = CookieOptimizer(input, max_calories=500)

        recipe = optimizer.optimal_recipe()
        assert recipe is not None
        score = optimizer.score(recipe)

        log.log(log.RESULT, f'The optimal cookie recipe score {score}: {recipe}')
        return score


part = Part2()

part.add_result(57600000, """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""")

part.add_result(15862900)
