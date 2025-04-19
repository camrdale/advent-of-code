from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day19.shared import BLUEPRINT, Blueprint, GeodeMaximizer, State


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_parsed_input(BLUEPRINT)

        multiplied_geodes = 1
        for blueprint_match in input[:3]:
            blueprint = Blueprint.from_match(blueprint_match)

            maximizer = GeodeMaximizer(blueprint)
            geodes = maximizer.most_geodes(0, State.initial_state(32))
            
            log.log(log.INFO, f'Blueprint {blueprint.num} created {geodes} geodes')
            multiplied_geodes *= geodes
        
        log.log(log.RESULT, f'The product of the number of geodes for the first 3 blueprints: {multiplied_geodes}')
        return multiplied_geodes


part = Part2()

# Works, but is too slow to run frequently.
# part.add_result(56*62, r"""
# Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
# Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
# """)

part.add_result(5800)
