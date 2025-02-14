import collections
import math
from typing import NamedTuple, Self


class ChemicalQuantity(NamedTuple):
    chemical: str
    amount: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        parts = text.strip().split()
        return cls(parts[1], int(parts[0]))


class Formula(NamedTuple):
    output: ChemicalQuantity
    inputs: list[ChemicalQuantity]

    @classmethod
    def from_text(cls, text: str) -> Self:
        index = text.find('=>')
        ingredients = text[:index].split(',')
        result = text[index+2:]
        return cls(
            ChemicalQuantity.from_text(result),
            [ChemicalQuantity.from_text(ingredient) for ingredient in ingredients])


def ore_for_fuel(formulas: dict[str, Formula], fuel: int) -> int:
    needed: dict[str, int] = collections.defaultdict(int)
    needed['FUEL'] = fuel
    ore = 0
    leftovers: dict[str, int] = collections.defaultdict(int)
    while needed:
        chemical, amount = needed.popitem()
        
        if chemical in leftovers:
            if amount >= leftovers[chemical]:
                amount -= leftovers[chemical]
                del leftovers[chemical]
            else:
                leftovers[chemical] -= amount
                amount = 0
        if amount == 0:
            continue
        
        formula = formulas[chemical]
        multiplier = math.ceil(amount / formula.output.amount)
        leftovers[chemical] += multiplier * formula.output.amount - amount
        for input in formula.inputs:
            if input.chemical == 'ORE':
                ore += multiplier * input.amount
                continue
            needed[input.chemical] += multiplier * input.amount
    return ore
