import heapq
import re
from typing import NamedTuple

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


MACHINE = re.compile(r'\[([.#]*)\] ([0-9,\(\) ]*) \{([0-9,]*)\}')


class State(NamedTuple):
    num_presses: int
    indicators: tuple[bool, ...]


def fewest_presses(target_indicators: tuple[bool, ...], buttons: list[tuple[int, ...]]) -> int:
    visited: set[tuple[bool, ...]] = set()
    states_to_try: list[State] = []
    heapq.heappush(states_to_try, State(0, (False,) * len(target_indicators)))

    while states_to_try:
        state = heapq.heappop(states_to_try)
        if state.indicators in visited:
            continue
        visited.add(state.indicators)

        if state.indicators == target_indicators:
            # Can only visit the ending location once, so the first time is the shortest path.
            return state.num_presses

        for button in buttons:
            indicators = list(state.indicators)
            for button_change in button:
                indicators[button_change] = not indicators[button_change]
            heapq.heappush(states_to_try, State(state.num_presses + 1, tuple(indicators)))

    raise ValueError(f'Failed to find path to the target: {target_indicators}')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_presses = 0
        for line in input:
            machine = MACHINE.fullmatch(line)
            assert machine is not None, line

            indicators = tuple(light == '#' for light in machine.group(1))
            buttons: list[tuple[int, ...]] = []
            for button_input in machine.group(2).split():
                buttons.append(tuple(map(int, button_input[1:-1].split(','))))
            
            total_presses += fewest_presses(indicators, buttons)

        log.log(log.RESULT, f'The fewest total presses to configure all machines: {total_presses}')
        return total_presses


part = Part1()

part.add_result(7, """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""")

part.add_result(545)
