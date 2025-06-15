import re
from typing import NamedTuple, Self


INGREDIENT = re.compile(r'(.*): capacity ([0-9-]*), durability ([0-9-]*), flavor ([0-9-]*), texture ([0-9-]*), calories ([0-9-]*)')


class Ingredient(NamedTuple):
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        m = INGREDIENT.match(text)
        assert m is not None
        return cls(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))


class CookieOptimizer:
    def __init__(self, input: list[str], max_calories: int | None = None) -> None:
        self.max_calories = max_calories
        self.ingredients: dict[str, Ingredient] = {}
        for line in input:
            ingredient = Ingredient.from_text(line)
            self.ingredients[ingredient.name] = ingredient

    def score(self, ingredient_amounts: dict[str, int]) -> int:
        assert len(ingredient_amounts) == len(self.ingredients), f'{ingredient_amounts} != {self.ingredients}'
        capacity = max(0, sum(
            amount * self.ingredients[ingredient].capacity
            for ingredient, amount in ingredient_amounts.items()))
        durability = max(0, sum(
            amount * self.ingredients[ingredient].durability
            for ingredient, amount in ingredient_amounts.items()))
        flavor = max(0, sum(
            amount * self.ingredients[ingredient].flavor
            for ingredient, amount in ingredient_amounts.items()))
        texture = max(0, sum(
            amount * self.ingredients[ingredient].texture
            for ingredient, amount in ingredient_amounts.items()))
        return capacity * durability * flavor * texture

    def optimal_recipe(self, chosen_ingredients: dict[str, int] | None = None) -> dict[str, int] | None:
        if chosen_ingredients is None:
            chosen_ingredients = {}
        
        remaining_size = 100 - sum(chosen_ingredients.values())
        remaining_ingredients = self.ingredients.keys() - chosen_ingredients.keys()
        ingredient = next(iter(remaining_ingredients))
        ingredients = dict(chosen_ingredients)

        remaining_calories = None
        if self.max_calories is not None:
            remaining_calories = self.max_calories - sum(
                amount * self.ingredients[ingredient].calories
                for ingredient, amount in chosen_ingredients.items())
        
        if len(remaining_ingredients) == 1:
            if remaining_calories is not None and remaining_size * self.ingredients[ingredient].calories > remaining_calories:
                return None
            ingredients[ingredient] = remaining_size
            return ingredients
        
        optimal_score = 0
        optimal_recipe: dict[str, int] | None = None
        for amount in range(0, remaining_size + 1):
            if remaining_calories is not None and amount * self.ingredients[ingredient].calories > remaining_calories:
                break
            ingredients[ingredient] = amount
            recipe = self.optimal_recipe(ingredients)
            if recipe is not None:
                score = self.score(recipe)
                if score >= optimal_score:
                    optimal_score = score
                    optimal_recipe = recipe

        return optimal_recipe
