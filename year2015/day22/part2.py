from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day22.shared import GameState, min_mana_to_win


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        mana = min_mana_to_win(GameState.initial(input), hard=True)

        if mana is None:
            raise ValueError(f'Failed to find a win for the player')

        log.log(log.RESULT, f'Minimum mana to win: {mana}')
        return mana


part = Part2()

part.add_result(1309)
