from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day19.shared import BLUEPRINT, Blueprint, State, GeodeMaximizer


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_parsed_input(BLUEPRINT)

        quality_levels = 0
        for blueprint_match in input:
            blueprint = Blueprint.from_match(blueprint_match)

            maximizer = GeodeMaximizer(blueprint)
            geodes = maximizer.most_geodes(0, State.initial_state(24))

            log.log(log.INFO, f'Blueprint {blueprint.num} created {geodes} geodes and has quality level: {blueprint.num*geodes}')
            quality_levels += blueprint.num*geodes
        
        log.log(log.RESULT, f'The sum of the quality levels for all the blueprints: {quality_levels}')
        return quality_levels


part = Part1()

part.add_result(33, r"""
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""")

part.add_result(1266)
