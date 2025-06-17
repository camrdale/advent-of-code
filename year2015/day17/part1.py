import functools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


@functools.cache
def fit(size: int, containers: tuple[int, ...]) -> int:
    if size == 0:
        return 1
    num_ways = 0
    for i, container in enumerate(containers):
        if container <= size:
            num_ways += fit(size - container, containers[i+1:])
    return num_ways


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        eggnog = parser.get_additional_params()[0]

        containers = tuple(sorted(list(map(int, input)), reverse=True))

        num_ways = fit(eggnog, containers)

        log.log(log.RESULT, f'The number of ways to fit all {eggnog} liters of eggnog: {num_ways}')
        return num_ways


part = Part1()

part.add_result(4, """
20
15
10
5
5
""", 25)

part.add_result(4372, None, 150)
