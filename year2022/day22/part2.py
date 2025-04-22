from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day22.shared import MonkeyMap, parse_path


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        map_input, path_input = parser.get_two_part_input()
        test = parser.get_additional_params()[0]

        monkey_map = MonkeyMap(map_input)
        if test:
            monkey_map.calculate_test_cube_wrapping()
        else:
            monkey_map.calculate_final_cube_wrapping()

        path = parse_path(path_input[0])
        for path_element in path:
            if type(path_element) is int:
                monkey_map.move(path_element)
            elif type(path_element) is str:
                monkey_map.turn(path_element)
        
        log.log(log.DEBUG, monkey_map.print_path())

        password = monkey_map.final_password()
        log.log(log.RESULT, f'The final password is: {password}')
        return password


part = Part2()

part.add_result(5031, r"""
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""", True)

part.add_result(124302, None, False)
