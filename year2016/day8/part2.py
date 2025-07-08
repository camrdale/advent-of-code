from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day8.shared import parse_instructions


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        display = parse_instructions(input)
        
        output = '\n'
        for row in display:
            output += ''.join([u'\u2588' if val else ' ' for val in row])
            output += '\n'

        log.log(log.RESULT, f'The displayed code is:{output}')
        return output


part = Part2()

part.add_result("""
████ ████ █  █ ████  ███ ████  ██   ██  ███   ██  
   █ █    █  █ █    █    █    █  █ █  █ █  █ █  █ 
  █  ███  ████ ███  █    ███  █  █ █    █  █ █  █ 
 █   █    █  █ █     ██  █    █  █ █ ██ ███  █  █ 
█    █    █  █ █       █ █    █  █ █  █ █    █  █ 
████ █    █  █ █    ███  █     ██   ███ █     ██  
""")
