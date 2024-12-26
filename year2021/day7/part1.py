from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        positions = [int(i) for i in input[0].split(',')]
        positions.sort()

        log(DEBUG, 'Number of crabs:', len(positions))
        log(DEBUG, 'Leftmost position:', positions[0])
        log(DEBUG, 'Rightmost position:', positions[-1])

        left_positions_num = 0
        left_positions_sum = 0
        right_positions_num = len(positions)
        right_positions_sum = sum(positions)
        current_position = 0
        current_position_num = 0
        min_sum = left_positions_sum + right_positions_sum
        min_position = 0

        new_position = positions[0]
        while positions:
            left_positions_sum += left_positions_num * (new_position - current_position)
            left_positions_num += current_position_num
            left_positions_sum += current_position_num * (new_position - current_position)

            current_position_num = 0
            while positions and positions[0] == new_position:
                positions.pop(0)
                current_position_num += 1
                right_positions_num -= 1
                right_positions_sum -= (new_position - current_position)

            right_positions_sum -= right_positions_num * (new_position - current_position)
            current_position = new_position
            if left_positions_sum + right_positions_sum <= min_sum:
                min_sum = left_positions_sum + right_positions_sum
                min_position = current_position
            else:
                break

            log(DEBUG,
                'Curent Position:', current_position, left_positions_sum + right_positions_sum,
                'Left:', left_positions_num, left_positions_sum,
                'Current:', current_position_num,
                'Right:', right_positions_num, right_positions_sum) #, positions)
            new_position += 1

        log(RESULT, 'Min cost of', min_sum, 'found at position', min_position)
        return min_sum


part = Part1()

part.add_result(37, """
16,1,2,0,4,2,7,1,2,14
""")

part.add_result(344605)
