from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        num_steps = int(parser.get_input()[0])

        position = 0
        last_1_insert = -1
        i = 0
        while i <= 50_000_000:
            # Repeat the following n times to get to the next time past the end of the list
            # for i in range(...): position = (position + num_steps) % i + 1
            n = (i - position) // num_steps + 1
            i += n
            position = (position + n * (num_steps + 1) - 1) % i + 1

            if position == 1:
                last_1_insert = i
        
        log.log(log.RESULT, f'The value after 0 in the circular buffer: {last_1_insert}')
        return last_1_insert


part = Part2()

part.add_result(34334221, """
348
""")
