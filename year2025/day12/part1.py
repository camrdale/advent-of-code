from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        shapes: dict[int, int] = {}
        for shape in input[:-1]:
            shape_id = int(shape[0].split(':')[0])
            shapes[shape_id] = 0
            for line in shape[1:]:
                shapes[shape_id] += line.count('#')

        num_fit = 0
        for line in input[-1]:
            size, shape_input = line.split(': ')
            width, height = map(int, size.split('x'))
            shape_nums = list(map(int, shape_input.split()))

            needed_squares = sum(shapes[shape_id] * num_shape for shape_id, num_shape in enumerate(shape_nums))
            if width * height < needed_squares:
                log.log(log.INFO, f'Cannot fit, need {needed_squares} but only have {width*height}: {line}')
                continue

            num_shapes = sum(shape_nums)
            if (width // 3) * (height // 3) >= num_shapes:
                log.log(log.INFO, f'Fits trivially, have room for {(width // 3) * (height // 3)} and only have {num_shapes}: {line}')
                num_fit += 1
                continue

            raise ValueError(f'Failed to trivally determine a fit for: {line}')

        log.log(log.RESULT, f'The number of trees that the presents can fit in: {num_fit}')
        return num_fit


part = Part1()

# Example is unsolvable

part.add_result(469)
