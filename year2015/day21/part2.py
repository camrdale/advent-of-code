from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day21.shared import Character, all_loadouts, fight


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        boss = Character.from_input(input)

        for loadout in all_loadouts()[::-1]:
            player = Character.from_loadout(100, loadout)
            boss.reset()
            if not fight(player, boss):
                log.log(log.RESULT, f'Most expensive loadout that loses is {loadout.cost()}')
                return loadout.cost()
        
        raise ValueError(f'Failed to lose to the boss with any loadout.')


part = Part2()

part.add_result(158)
