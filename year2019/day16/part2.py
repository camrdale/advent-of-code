import aoc.input
from aoc import log
from aoc import runner


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        input_list = list(map(int, input[0]))
        n = len(input_list)

        offset = int(''.join(map(str, input_list[:7])))
        num_digits = n*10000 - offset
        log.log(log.INFO, f'Message offet is {offset} into {n*10000} digit list, leaving {num_digits} digits to calculate')
        if offset <= (n*10000) // 2:
            raise ValueError(f'Offset {offset} is too small, needs to be greater than {(n*10000) // 2}')

        l = input_list[-(num_digits % n):] + input_list*(num_digits // n)
        for _ in range(100):
            for i in range(num_digits-2, -1, -1):
                l[i] = abs(l[i] + l[i+1]) % 10

        log.log(log.RESULT, f'After repeating 10000 times, 8 digits at offset {offset} after 100 phases: {"".join(map(str, l[:8]))}')
        return int(''.join(map(str, l[:8])))


part = Part2()

part.add_result(84462026, r"""
03036732577212944063491565474664
""")

part.add_result(78725270, r"""
02935109699940807407585447034323
""")

part.add_result(53553731, r"""
03081770884921959731165446850517
""")

part.add_result(55005000)
