import heapq

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day7.shared import Step


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        steps = Step.from_input(input)

        ready: list[str] = []
        for step in steps.values():
            if not step.requirements:
                heapq.heappush(ready, step.id)
        
        completed = ''
        while ready:
            next = steps[heapq.heappop(ready)]
            completed += next.id
            for now_ready in next.complete(steps):
                heapq.heappush(ready, now_ready)

        log.log(log.RESULT, f'The order the steps should be completed: "{completed}"')
        return ''.join(completed)


part = Part1()

part.add_result('CABDFE', """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""")

part.add_result('CQSWKZFJONPBEUMXADLYIGVRHT')
