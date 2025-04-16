from collections import defaultdict
import re
from typing import NamedTuple, Self

from aoc.input import InputParser


VALVE = re.compile(r'Valve ([A-Z]*) has flow rate=([0-9]*); tunnels? leads? to valves? ([A-Z, ]*)')


class Valve(NamedTuple):
    name: str
    flow_rate: int

    @classmethod
    def from_valve_input(cls, valve_input: tuple[str, ...]) -> Self:
        return cls(valve_input[0], int(valve_input[1]))
    
    def __repr__(self) -> str:
        return f'{self.name}-{self.flow_rate}'


class ValveNetwork:
    def __init__(self, parser: InputParser):
        input = parser.get_parsed_input(VALVE)
        self.valves: dict[str, Valve] = {}
        neighbors: dict[str, list[str]] = {}
        for valve_input in input:
            valve = Valve.from_valve_input(valve_input)
            if valve.name == 'AA' or valve.flow_rate > 0:
                self.valves[valve.name] = valve
            neighbors[valve.name] = valve_input[2].split(', ')

        # Calculate distances between valves that have flow, and 'AA'.
        self.valve_distances: dict[tuple[str, str], int] = defaultdict(lambda: 100)
        for valve in self.valves.values():
            for neighbor in neighbors[valve.name]:
                location = valve.name
                distance = 1
                while neighbor not in self.valves:
                    neighbor_neighbors = [next_neighbor for next_neighbor in neighbors[neighbor] if next_neighbor != location]
                    assert len(neighbor_neighbors) == 1, f'{location}, {neighbor}, {neighbor_neighbors}'
                    location = neighbor
                    neighbor = neighbor_neighbors[0]
                    distance += 1
                self.valve_distances[valve.name, neighbor] = distance

        # Calculate minimum distances between all valves that have flow, and 'AA'.
        for valve_a in self.valves:
            for valve_b in self.valves:
                for valve_c in self.valves:
                    if valve_c != valve_b:
                        self.valve_distances[valve_b, valve_c] = min(
                            self.valve_distances[valve_b, valve_c],
                            self.valve_distances[valve_b, valve_a] + self.valve_distances[valve_a, valve_c])
        # Remove AA so it is not considered as a target for a move.
        del self.valves['AA']

    def optimal_pressure(self, location: str, opened_valves: frozenset[str], time_remaining: int) -> tuple[int, frozenset[str]]:
        optimal_pressure = 0
        optimal_valves: frozenset[str] = opened_valves
        for valve in self.valves:
            if valve in opened_valves:
                continue
            distance = self.valve_distances[location, valve]
            new_time_remaining = time_remaining - distance - 1
            if new_time_remaining <= 0:
                continue
            next_pressure, next_opened_valves = self.optimal_pressure(valve, opened_valves.union([valve]), new_time_remaining)
            pressure = new_time_remaining * self.valves[valve].flow_rate + next_pressure
            if pressure > optimal_pressure:
                optimal_pressure = pressure
                optimal_valves = next_opened_valves.union([valve])
        return optimal_pressure, optimal_valves
