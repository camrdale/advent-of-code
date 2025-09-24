from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day24.shared import ImmuneSystemSimulator


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        immune_input, infection_input = parser.get_two_part_input()

        simulator = ImmuneSystemSimulator(immune_input[1:], infection_input[1:])

        simulator.combat()

        remaining_units = simulator.remaining_units()

        log.log(log.RESULT, f'The result of the combat after {simulator.rounds} completed rounds: {remaining_units}')
        return remaining_units


part = Part1()

part.add_result(5216, """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""")

part.add_result(16747)
