from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        bus_ids: list[tuple[int, int]] = [
            (i, int(bus))
            for i, bus in enumerate(input[1].split(','))
            if bus != 'x'
        ]

        start = 0
        multiplier = bus_ids[0][1]

        for bus_index, bus_id in bus_ids[1:]:
            for time in range(start, start + multiplier * bus_id, multiplier):
                if (time + bus_index) % bus_id == 0:
                    start = time
                    multiplier *= bus_id
                    break
            else:
                raise ValueError(f'Failed to find a time that {bus_id} with index {bus_index} fits into {start} plus {multiplier}')

        log.log(log.RESULT, f'First time when buses arrive at their indexes in the list: {start}')
        return start


part = Part2()

part.add_result(1068781, """
939
7,13,x,x,59,x,31,19
""")

part.add_result(3417, """
939
17,x,13,19
""")

part.add_result(754018, """
939
67,7,59,61
""")

part.add_result(779210, """
939
67,x,7,59,61
""")

part.add_result(1261476, """
939
67,7,x,59,61
""")

part.add_result(1202161486, """
939
1789,37,47,1889
""")

part.add_result(552612234243498)
