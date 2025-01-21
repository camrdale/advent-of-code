import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2023.day21 import shared


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        map = shared.GardenMap(input)

        log.log(log.DEBUG, f'Staring coord: {map.starting_point}, grid = {map.width}x{map.height}')
        num_column = 0
        num_row = 0
        for rock in map.features['#']:
            if rock.x == map.starting_point.x:
                num_column += 1
            if rock.y == map.starting_point.y:
                num_row += 1
        log.log(log.DEBUG, f'Num rocks in same row {num_row}, same column {num_column} as starting coord')

        total_reachable_plots = 0
        num_steps = 26501365

        # A lot of squares have all their plots reachable, but there are two possibilities for even/odd steps.
        even_reachable = map.reachable_plots(map.starting_point, num_steps - 1)
        log.log(log.DEBUG, map.print_map({'O': even_reachable}))
        even_full_squares = len(even_reachable)

        odd_reachable = map.reachable_plots(map.starting_point, num_steps)
        log.log(log.DEBUG, map.print_map({'O': odd_reachable}))
        odd_full_squares = len(odd_reachable)

        # n is the number of full squares in any direction, including the starting square
        n = ((num_steps - 65) // 131) # 202300
        num_even_full_squares = n**2  # 40925290000
        num_odd_full_squares = (n-1)**2  # 40924885401
        total_reachable_plots += num_odd_full_squares * odd_full_squares + num_even_full_squares * even_full_squares

        # At the ends of the squares that are fully reachable are 4 where we start in the middle of one side.
        remaining_steps = 130  # 26501365 − 66 − (131×202299)
        total_reachable_plots += len(map.reachable_plots(map.starting_point._replace(y=0), remaining_steps))
        total_reachable_plots += len(map.reachable_plots(map.starting_point._replace(y=map.height-1), remaining_steps))
        reachable = map.reachable_plots(map.starting_point._replace(x=0), remaining_steps)
        total_reachable_plots += len(reachable)
        log.log(log.DEBUG, map.print_map({'O': reachable}))
        total_reachable_plots += len(map.reachable_plots(map.starting_point._replace(x=map.width-1), remaining_steps))

        # There are also n each small corner squares where we have to start in each corner.
        remaining_steps -= 66  # 66 steps to get to the small corner square's corner
        reachable = map.reachable_plots(aoc.map.Coordinate(0, 0), remaining_steps)
        total_reachable_plots += n * len(reachable)
        log.log(log.DEBUG, map.print_map({'O': reachable}))
        total_reachable_plots += n * len(map.reachable_plots(aoc.map.Coordinate(0, map.height - 1), remaining_steps))
        total_reachable_plots += n * len(map.reachable_plots(aoc.map.Coordinate(map.width - 1, 0), remaining_steps))
        total_reachable_plots += n * len(map.reachable_plots(aoc.map.Coordinate(map.width - 1, map.height - 1), remaining_steps))

        # And (n - 1) each large corner squares where we have to start in each corner.
        remaining_steps += 131  # width/height less steps to get back to the previous large square's corner
        reachable = map.reachable_plots(aoc.map.Coordinate(0, 0), remaining_steps)
        total_reachable_plots += (n - 1) * len(reachable)
        log.log(log.DEBUG, map.print_map({'O': reachable}))
        total_reachable_plots += (n - 1) * len(map.reachable_plots(aoc.map.Coordinate(0, map.height - 1), remaining_steps))
        total_reachable_plots += (n - 1) * len(map.reachable_plots(aoc.map.Coordinate(map.width - 1, 0), remaining_steps))
        total_reachable_plots += (n - 1) * len(map.reachable_plots(aoc.map.Coordinate(map.width - 1, map.height - 1), remaining_steps))

        log.log(log.RESULT, f'Reachable plots in {num_steps} steps: {total_reachable_plots}')
        return total_reachable_plots


part = Part2()

part.add_result(605247138198755)
