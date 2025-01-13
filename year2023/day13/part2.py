from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part


def transpose(pattern: list[str]) -> list[str]:
    transposed: list[str] = []
    for i in range(len(pattern[0])):
        transposed.append(''.join(line[i] for line in pattern))
    return transposed


def one_error_in_reflection(pattern: list[str], row: int) -> bool:
    num_errors = 0
    reflected_row = row + 1
    while row >= 0 and reflected_row < len(pattern) and num_errors <= 1:
        num_errors += sum(c1 != c2 for c1, c2 in zip(pattern[row], pattern[reflected_row]))
        row -= 1
        reflected_row += 1
    return num_errors == 1


def check_rows(pattern: list[str]) -> int | None:
    for row in range(len(pattern) - 1):
        if one_error_in_reflection(pattern, row):
            return row
    return None


class Part2(Part):
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


part = Part2()

part.add_result(400, """
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

part.add_result(34795)
