import functools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


@functools.cache
def fit(size: int, containers: tuple[int, ...]) -> tuple[int, int]:
    if size == 0:
        return 0, 1
    num_ways = 0
    min_containers = 100000
    for i, container in enumerate(containers):
        if container <= size:
            next_min_containers, next_num_ways = fit(size - container, containers[i+1:])
            if next_min_containers + 1 < min_containers:
                num_ways = next_num_ways
                min_containers = next_min_containers + 1
            elif next_min_containers + 1 == min_containers:
                num_ways += next_num_ways
    return min_containers, num_ways


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        eggnog = parser.get_additional_params()[0]

        containers = tuple(sorted(list(map(int, input)), reverse=True))

        min_containers, num_ways = fit(eggnog, containers)

        log.log(log.RESULT, f'The number of ways to fit all {eggnog} liters of eggnog in {min_containers} containers: {num_ways}')
        return num_ways


part = Part2()

part.add_result(3, """
20
15
10
5
5
""", 25)

part.add_result(4, None, 150)
