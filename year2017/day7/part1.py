from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day7.shared import Program


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        tower = Program.create_tower(input)

        log.log(log.RESULT, f'The name of the bottom program is: {tower.name}')
        return tower.name


part = Part1()

part.add_result('tknk', """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
""")

part.add_result('ahnofa')
