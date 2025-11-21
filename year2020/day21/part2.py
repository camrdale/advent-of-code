from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day21.shared import parse_ingredients

class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        _, known_allergens = parse_ingredients(input)

        dangerous_ingredients = ','.join([
            ingredient
            for _, ingredient in sorted(known_allergens.items())
        ])

        log.log(log.RESULT, f'The list of dangerous ingredients: {dangerous_ingredients}')
        return dangerous_ingredients


part = Part2()

part.add_result('mxmxvkd,sqjhc,fvjkl', """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""")

part.add_result('vpzxk,bkgmcsx,qfzv,tjtgbf,rjdqt,hbnf,jspkl,hdcj')
