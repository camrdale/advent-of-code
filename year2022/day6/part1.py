from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day6.shared import find_n_distinct_characters


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        start_of_packet = find_n_distinct_characters(input, 4)
        log.log(log.RESULT, f'The start-of-packet marker occurs after character: {start_of_packet}')
        return start_of_packet


part = Part1()

part.add_result(7, r"""
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""")

part.add_result(5, r"""
bvwbjplbgvbhsrlpgdmjqwftvncz
""")

part.add_result(6, r"""
nppdvjthqldpwncqszvftbrmjlhg
""")

part.add_result(10, r"""
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
""")

part.add_result(11, r"""
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
""")

part.add_result(1760)
