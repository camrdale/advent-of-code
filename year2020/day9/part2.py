from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day9.shared import xmas_invalid


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        preamble: int = parser.get_additional_params()[0]

        data = list(map(int, input))
        invalid = xmas_invalid(data, preamble)

        for i in range(len(data)):
            j = 1
            sum = data[i]
            while i + j < len(data) and sum < invalid:
                sum += data[i+j]
                if sum == invalid:
                    weakness = min(data[i:i+j+1]) + max(data[i:i+j+1])
                    log.log(log.RESULT, f'The range that sums to {invalid} is {data[i]}-{data[i+j]} with weakness: {weakness}')
                    return weakness
                j += 1
        
        raise ValueError(f'Failed to find contiguous set of numbers that sum to {invalid}')


part = Part2()

part.add_result(62, """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
""", 5)

part.add_result(4830226, None, 25)
