import aoc.input
from aoc import log
from aoc import runner


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        input_list = list(map(int, input[0]))

        n = len(input_list)
        multipliers: list[list[int]] = []
        for i in range(n):
            multipliers.append((([0]*(i+1) + [1]*(i+1) + [0]*(i+1) + [-1]*(i+1))*(n//(4*(i+1))+1))[1:n+1])

        l = list(input_list)
        for _ in range(100):
            next_list: list[int] = []
            for i in range(n):
                next_list.append(abs(sum(a*b for a,b in zip(l, multipliers[i]))) % 10)
            l = next_list

        log.log(log.INFO, ''.join(map(str, l)))
        log.log(log.RESULT, f'First 8 digits after 100 phases: {"".join(map(str, l[:8]))}')
        return int(''.join(map(str, l[:8])))


part = Part1()

part.add_result(24176176, r"""
80871224585914546619083218645595
""")

part.add_result(73745418, r"""
19617804207202209144916044189917
""")

part.add_result(52432133, r"""
69317163492948606335995924319873
""")

part.add_result(11833188)
