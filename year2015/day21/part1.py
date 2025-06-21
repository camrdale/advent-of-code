from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day21.shared import Character, all_loadouts, fight


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        boss = Character.from_input(input)

        for loadout in all_loadouts():
            player = Character.from_loadout(100, loadout)
            boss.reset()
            if fight(player, boss):
                log.log(log.RESULT, f'Cheapest loadout to beat the boss is {loadout.cost()}')
                return loadout.cost()
        
        raise ValueError(f'Failed to beat the boss with any loadout.')


part = Part1()

part.add_result(91)
