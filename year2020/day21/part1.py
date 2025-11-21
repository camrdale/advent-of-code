from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day21.shared import parse_ingredients

class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        all_ingredients, known_allergens = parse_ingredients(input)

        known_ingredients = set(known_allergens.values())
        num_allergen_free = 0
        for ingredients in all_ingredients:
            num_allergen_free += len(ingredients - known_ingredients)

        log.log(log.RESULT, f'The number of allergen free ingredients that appear: {num_allergen_free}')
        return num_allergen_free


part = Part1()

part.add_result(5, """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""")

part.add_result(2150)
