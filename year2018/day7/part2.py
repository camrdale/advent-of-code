import heapq

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day7.shared import Step


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        num_workers: int = parser.get_additional_params()[0]
        base_time: int = parser.get_additional_params()[1]

        steps = Step.from_input(input, base_time=base_time)

        ready: list[str] = []
        for step in steps.values():
            if not step.requirements:
                heapq.heappush(ready, step.id)
        
        processing: list[str] = []
        num_seconds = 0
        while ready or processing:
            while ready and len(processing) < num_workers:
                next = steps[heapq.heappop(ready)]
                processing.append(next.id)

            for id in list(processing):
                steps[id].time_to_complete -= 1
                if steps[id].time_to_complete == 0:
                    processing.remove(id)
                    for now_ready in steps[id].complete(steps):
                        heapq.heappush(ready, now_ready)

            num_seconds += 1

        log.log(log.RESULT, f'The number of seconds to complete all the steps: {num_seconds}')
        return num_seconds


part = Part1()

part.add_result(15, """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""", 2, 0)

part.add_result(914, None, 5, 60)
