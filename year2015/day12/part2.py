import json
from typing import Any, cast

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


def sum_dict(data: dict[str, Any]) -> int:
    for _, value in data.items():
        if value == 'red':
            return 0
    return sum(sum_json(value) for value in data.values())


def sum_array(data: list[Any]) -> int:
    return sum(sum_json(element) for element in data)


def sum_json(data: Any) -> int:
    if type(data) == list:
        return sum_array(cast(list[Any], data))
    if type(data) == dict:
        return sum_dict(cast(dict[str, Any], data))
    if type(data) == int:
        return data
    return 0


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        data = json.loads(input[0])
        total = sum_json(data)

        log.log(log.RESULT, f'The sum of all non-red numbers: {total}')
        return total


part = Part2()

part.add_result(6, """
[1,2,3]
""")

part.add_result(4, """
[1,{"c":"red","b":2},3]
""")

part.add_result(0, """
{"d":"red","e":[1,2,3,4],"f":5}
""")

part.add_result(6, """
[1,"red",5]
""")

part.add_result(65402)
