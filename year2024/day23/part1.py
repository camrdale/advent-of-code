from collections import defaultdict

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        downstream_computers: dict[str, set[str]] = defaultdict(set)
        for line in input:
            comp1, comp2 = sorted(line.split('-'))
            downstream_computers[comp1].add(comp2)

        log(DEBUG, f'{len(downstream_computers)} unique computers with max set:', max(len(s) for s in downstream_computers.values()))

        sets_of_3_with_t = 0
        for computer, connected_computers in sorted(downstream_computers.items()):
            for connected_computer in sorted(connected_computers):
                for third_computer in sorted(connected_computers.intersection(downstream_computers[connected_computer])):
                    if computer[0] == 't' or connected_computer[0] == 't' or third_computer[0] == 't':
                        log(INFO, f'Found set of 3 with a t: {computer},{connected_computer},{third_computer}')
                        sets_of_3_with_t += 1
                    else:
                        log(DEBUG, f'Found set of 3: {computer},{connected_computer},{third_computer}')
        
        log(RESULT, f'Sets of 3 that contain a t: {sets_of_3_with_t}')
        return sets_of_3_with_t


part = Part1()

part.add_result(7, """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""")

part.add_result(1098)
