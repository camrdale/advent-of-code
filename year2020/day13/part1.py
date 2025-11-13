from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        time = int(input[0])

        wait_time, bus_id = min([
            (int(bus) - time % int(bus), int(bus))
            for bus in input[1].split(',')
            if bus != 'x'
        ])

        log.log(log.RESULT, f'Bus {bus_id} arrives in {wait_time} minutes: {bus_id * wait_time}')
        return bus_id * wait_time


part = Part1()

part.add_result(295, """
939
7,13,x,x,59,x,31,19
""")

part.add_result(2305)
