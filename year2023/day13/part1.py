from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part


def transpose(pattern: list[str]) -> list[str]:
    transposed: list[str] = []
    for i in range(len(pattern[0])):
        transposed.append(''.join(line[i] for line in pattern))
    return transposed


def is_reflection(pattern: list[str], row: int) -> bool:
    reflected_row = row + 1
    while row >= 0 and reflected_row < len(pattern):
        if pattern[row] != pattern[reflected_row]:
            return False
        row -= 1
        reflected_row += 1
    return True


def check_rows(pattern: list[str]) -> int | None:
    for row in range(len(pattern) - 1):
        if is_reflection(pattern, row):
            return row
    return None


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        notes_summary = 0
        for pattern in input:
            reflection_row = check_rows(pattern)
            if reflection_row is not None:
                log(INFO, f'Found reflection on horizontal line between rows {reflection_row+1} and {reflection_row+2}')
                notes_summary += 100 * (reflection_row + 1)
                continue
                
            pattern = transpose(pattern)
            reflection_row = check_rows(pattern)
            if reflection_row is not None:
                log(INFO, f'Found reflection on vertical line between columns {reflection_row+1} and {reflection_row+2}')
                notes_summary += reflection_row + 1
                continue

            print(f'ERROR: found no reflection in pattern:\n{pattern}')

        log(RESULT, f'Summary of all the notes: {notes_summary}')
        return notes_summary


part = Part1()

part.add_result(405, """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""")

part.add_result(35521)
