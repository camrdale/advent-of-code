from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day6.shared import find_n_distinct_characters


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        start_of_message = find_n_distinct_characters(input, 14)
        log.log(log.RESULT, f'The start-of-message marker occurs after character: {start_of_message}')
        return start_of_message


part = Part2()

part.add_result(19, r"""
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""")

part.add_result(23, r"""
bvwbjplbgvbhsrlpgdmjqwftvncz
""")

part.add_result(23, r"""
nppdvjthqldpwncqszvftbrmjlhg
""")

part.add_result(29, r"""
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
""")

part.add_result(26, r"""
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
""")

part.add_result(2974)
