from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

from .shared import Racetrack


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        racetrack = Racetrack(input)

        all_cheats = racetrack.all_cheats(20)

        for saved_time, cheats in sorted(all_cheats.items()):
            if saved_time >= 100:
                break
            log(INFO, f'There are {len(cheats)} cheats that save {saved_time} picoseconds.')

        cheats_100ps = sum(len(cheats) for saved_time, cheats in all_cheats.items() if saved_time >= 100)
        log(RESULT, 'Number of cheats that save at least 100ps:', cheats_100ps)

        best_cheat = sorted(all_cheats.items())[-1]
        log(DEBUG, f'Best cheats save {best_cheat[0]} picoseconds')
        log(DEBUG, racetrack.print_cheats(best_cheat[1]))

        return cheats_100ps


part = Part2()

part.add_result(0, """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""")

part.add_result(1022577)
