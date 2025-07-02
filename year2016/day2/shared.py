from collections import defaultdict

from aoc import log


def build_next_map(keypad: list[str]) -> dict[str, dict[str, str]]:
    """Build a map from the current position, given a direction, where is the next position."""
    next_map: dict[str, dict[str, str]] = {}
    for row, line in enumerate(keypad):
        for column, c in enumerate(line):
            if c.isalnum():
                directions: dict[str, str] = {'U': c, 'D': c, 'L': c, 'R': c}
                if row - 1 >= 0 and len(keypad[row - 1]) > column and keypad[row - 1][column].isalnum():
                    directions['U'] = keypad[row - 1][column]
                if row + 1 < len(keypad) and len(keypad[row + 1]) > column and keypad[row + 1][column].isalnum():
                    directions['D'] = keypad[row + 1][column]
                if column - 1 >= 0 and keypad[row][column - 1].isalnum():
                    directions['L'] = keypad[row][column - 1]
                if column + 1 < len(keypad[row]) and keypad[row][column + 1].isalnum():
                    directions['R'] = keypad[row][column + 1]
                next_map[c] = directions
    return next_map


def reverse_map(next_map: dict[str, dict[str, str]]) -> dict[str, dict[str, list[str]]]:
    """Reverse the next map, for walking backwards through the instructions."""
    reverse_next_map: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    for position, directions in next_map.items():
        for direction, next_position in directions.items():
            reverse_next_map[next_position][direction].append(position)

    return reverse_next_map


def code_digit_finder(
        instruction: str,
        reverse_next_map: dict[str, dict[str, list[str]]],
        starting: str) -> str:
    # The remaining possibilities while walking backwards through the instruction.
    # key is final position, value is list of current positions that would lead to final
    possibilities = {digit: [digit] for digit in reverse_next_map}

    for i, direction in enumerate(instruction[::-1]):
        next_possibilities: dict[str, list[str]] = defaultdict(list)
        for final_position, current_positions in possibilities.items():
            for current_position in current_positions:
                if direction in reverse_next_map[current_position]:
                    for previous_position in reverse_next_map[current_position][direction]:
                        next_possibilities[final_position].append(previous_position)
        possibilities = dict(next_possibilities)
        log.log(log.DEBUG, f'After {direction}, remaining possibilities are: {possibilities}')

        if len(possibilities) == 1:
            # Only one possible final position left, so it must be the code digit.
            digit = next(iter(possibilities.keys()))
            log.log(log.INFO, f'Found character "{digit}" after {i+1} iterations of {len(instruction)} possible ({1 - (i+1)/len(instruction):.1%} savings)')
            return digit

    # Failed to deduce the code digit, so determine which final position is associated with the starting position.
    from_starting = [
        final_position
        for final_position, current_positions in possibilities.items()
        if starting in current_positions]
    assert len(from_starting) == 1, from_starting
    log.log(log.INFO, f'Found character "{from_starting[0]}" after {len(instruction)} iterations')
    return from_starting[0]


def code_finder(instructions: list[str], keypad: str, starting: str) -> str:
    next_map = build_next_map(keypad.split('\n'))

    reverse_next_map = reverse_map(next_map)

    code = ''
    digit = starting
    for instruction in instructions:
        digit = code_digit_finder(instruction, reverse_next_map, digit)
        code += digit

    return code
