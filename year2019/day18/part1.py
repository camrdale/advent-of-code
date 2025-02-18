from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019.day18.shared import VaultMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = VaultMap(input)
        log.log(log.INFO, map.print_map())

        map.build_visited_sets()

        all_keys= frozenset(map.keys.keys())
        shortest_path = map.shortest_key_path(map.entrances, all_keys)

        log.log(log.RESULT, f'Shortest path to collect all keys: {shortest_path}')
        return shortest_path


part = Part1()

part.add_result(8, r"""
#########
#b.A.@.a#
#########
""")

part.add_result(86, r"""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""")

part.add_result(132, r"""
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""")

part.add_result(81, r"""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""")

part.add_result(136, r"""
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""")

part.add_result(3862)
