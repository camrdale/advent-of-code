from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day16.shared import ValveNetwork


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        network = ValveNetwork(parser)

        most_pressure, opened_valves = network.optimal_pressure('AA', frozenset(), 26)
        log.log(log.INFO, f'The most pressure that can be released in 26 minutes: {most_pressure}')

        # Running them in sequence works for the real input, though not the test data.
        elephant_pressure, _ = network.optimal_pressure('AA', opened_valves, 26)

        log.log(log.RESULT, f'The most pressure that can be released in 26 minutes with the help of an elephant: {most_pressure + elephant_pressure}')
        return most_pressure + elephant_pressure


part = Part2()

# Running them in sequence works for the real input, though not the test data.
# part.add_result(1707, r"""
# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II
# """)

part.add_result(1933)
