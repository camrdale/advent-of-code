from aoc import log


TRAPS: set[str] = set([
    '^^.',
    '.^^',
    '^..',
    '..^',
])


def count_safe_tiles(first_row: str, num_rows: int) -> int:
    num_safe = 0
    row = '.' + first_row + '.'
    num_safe += len(first_row) - row.count('^')
    log.log(log.INFO, row)

    for _ in range(num_rows - 1):
        row = ''.join('^' if row[i-1:i+2] in TRAPS else '.' for i in range(0, len(row)))
        num_safe += len(first_row) - row.count('^')
        log.log(log.INFO, row)

    return num_safe
