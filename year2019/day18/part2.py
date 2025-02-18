from aoc.input import InputParser
from aoc import log
from aoc.map import Offset
from aoc.runner import Part

from year2019.day18.shared import VaultMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = VaultMap(input)
        log.log(log.INFO, map.print_map())
        main_entrance = map.entrances[0]
        map.entrances = (
            main_entrance.add(Offset(-1,-1)),
            main_entrance.add(Offset(-1,1)),
            main_entrance.add(Offset(1,-1)),
            main_entrance.add(Offset(1,1))
        )
        map.features['#'].update([
            main_entrance,
            main_entrance.add(Offset(0,1)),
            main_entrance.add(Offset(1,0)),
            main_entrance.add(Offset(0,-1)),
            main_entrance.add(Offset(-1,0)),
        ])

        map.build_visited_sets()

        all_keys = frozenset(map.keys.keys())
        shortest_path = map.shortest_key_path(map.entrances, all_keys)

        log.log(log.RESULT, f'Shortest path to collect all keys: {shortest_path}')
        return shortest_path


part = Part2()

part.add_result(8, r"""
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
""")

part.add_result(24, r"""
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############
""")

part.add_result(32, r"""
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############
""")

part.add_result(72, r"""
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
""")

part.add_result(1626)
