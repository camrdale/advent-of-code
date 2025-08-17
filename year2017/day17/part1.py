from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        num_steps = int(parser.get_input()[0])

        buffer = [0]
        position = 0
        for i in range(1, 2018):
            position = (position + num_steps) % len(buffer) + 1
            buffer.insert(position, i)
        
        after_2017 = buffer[(position + 1) % len(buffer)]
        log.log(log.RESULT, f'The value after 2017 in the circular buffer: {after_2017}')
        return after_2017


part = Part1()

part.add_result(638, """
3
""")

part.add_result(417, """
348
""")
