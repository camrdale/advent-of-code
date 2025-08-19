from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day19.shared import follow_route


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        waypoints, _ = follow_route(input)
        
        log.log(log.RESULT, f'The waypoints found along the route: {waypoints}')
        return waypoints


part = Part1()

part.add_result('ABCDEF', """
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""")

part.add_result('LOHMDQATP')
