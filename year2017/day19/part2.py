from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day19.shared import follow_route


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        _, num_steps = follow_route(input)

        log.log(log.RESULT, f'The number of steps to complete the route: {num_steps}')
        return num_steps


part = Part2()

part.add_result(38, """
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""")

part.add_result(16492)
