from collections import defaultdict

from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.runner import Part


def longest_password(downstream_computers: dict[str, set[str]]) -> str:
    password = ''
    for computer, connected_computers in sorted(downstream_computers.items()):
        connected_downstream_computers: dict[str, set[str]] = defaultdict(set)
        for connected_computer in sorted(connected_computers):
            for third_computer in sorted(connected_computers.intersection(downstream_computers[connected_computer])):
                connected_downstream_computers[connected_computer].add(third_computer)
        if connected_downstream_computers:
            connected_password = longest_password(connected_downstream_computers)
            if len(connected_password) + 3 > len(password):
                password = computer + ',' + connected_password

    if password == '':
        # There's no sets of 3 remaining, return the password for one of the sets of 2.
        for computer, connected_computers in downstream_computers.items():
            if len(connected_computers) > 0:
                # Choose the first neighbor, doesn't matter which, they all would have the same password length
                connected_computer = next(iter(connected_computers))
                password = computer + ',' + connected_computer
                break

    assert password != ''
    return password


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        downstream_computers: dict[str, set[str]] = defaultdict(set)
        for line in input:
            comp1, comp2 = sorted(line.split('-'))
            downstream_computers[comp1].add(comp2)

        log(DEBUG, f'{len(downstream_computers)} unique computers with max set:', max(len(s) for s in downstream_computers.values()))

        password = longest_password(downstream_computers)
        
        log(RESULT, f'Password for the largest group is: {password}')
        return password


part = Part2()

part.add_result('co,de,ka,ta', """
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

part.add_result('ar,ep,ih,ju,jx,le,ol,pk,pm,pp,xf,yu,zg')
