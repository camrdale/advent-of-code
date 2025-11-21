from aoc import log


def parse_ingredients(input: list[str]) -> tuple[list[set[str]], dict[str, str]]:
    allergens: dict[str, set[str]] = {}
    all_ingredients: list[set[str]] = []
    for line in input:
        ingredient_input, allergen_input = line.split(' (contains ')
        ingredients = set(ingredient_input.split(' '))
        all_ingredients.append(ingredients.copy())
        for allergen in allergen_input[:-1].split(', '):
            if allergen in allergens:
                allergens[allergen].intersection_update(ingredients)
            else:
                allergens[allergen] = ingredients.copy()
    
    log.log(log.DEBUG, allergens)

    known_allergens: dict[str, str] = {}
    while allergens:
        progress = False
        for allergen, ingredients in list(allergens.items()):
            if len(ingredients) == 1:
                ingredient = next(iter(ingredients))
                known_allergens[allergen] = ingredient
                del allergens[allergen]
                for other_ingredients in allergens.values():
                    other_ingredients.discard(ingredient)
                progress = True
        if not progress:
            raise ValueError(f'Failed to progress:\n{known_allergens}\n{allergens}')

    log.log(log.INFO, known_allergens)

    return all_ingredients, known_allergens
