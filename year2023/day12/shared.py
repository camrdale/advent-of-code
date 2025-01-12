import functools

from aoc.log import log, DEBUG


def valid_damaged_arrangement(record: str, start: int, length: int) -> bool:
    end = start + length
    if any(c == '.' for c in record[start:end]):
        return False
    if end < len(record) and record[end] == '#':
        return False
    return True


@functools.cache
def possible_arrangements(record: str, damaged_springs: tuple[int, ...]) -> int:
    if len(damaged_springs) == 0:
        if any(c == '#' for c in record):
            return 0
        return 1
    
    damaged_length = damaged_springs[0]
    remaining_damaged = damaged_springs[1:]
    remaining_length = sum(remaining_damaged) + len(remaining_damaged)

    while len(record) > 0 and record[0] == '.':
        record = record[1:]
    log(DEBUG, f'For {record}, {1 + len(record) - remaining_length - damaged_length} squares are possible')
    
    possibilities = 0
    start = 0
    while start + damaged_length + remaining_length <= len(record):
        if valid_damaged_arrangement(record, start, damaged_length):
            num_possibilities = possible_arrangements(record[start+damaged_length+1:], remaining_damaged)
            log(DEBUG, f'Valid arrangement for {record} with length {damaged_length} is {start}: {num_possibilities} following possible arrangements')
            possibilities += num_possibilities
        if record[start] == '#':
            break
        start += 1

    return possibilities
