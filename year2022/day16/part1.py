from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day16.shared import ValveNetwork


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        network = ValveNetwork(parser)

        most_pressure, _ = network.optimal_pressure('AA', frozenset(), 30)

        log.log(log.RESULT, f'The most pressure that can be released in 30 minutes: {most_pressure}')
        return most_pressure


part = Part1()

part.add_result(1651, r"""
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""")

part.add_result(1376)
