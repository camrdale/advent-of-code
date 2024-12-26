from pathlib import Path
import subprocess

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        awk_file = Path(__file__).parent.resolve() / 'commands.awk'
        result = subprocess.run(args=[str(awk_file)], input='\n'.join(input), text=True, capture_output=True)

        log(INFO, result.stdout)
        answer = int([line for line in result.stdout.split('\n') if line.startswith('Part 2 Position*Depth')][0].split('=')[1])
        log(RESULT, 'horizontal position * depth:', answer)
        return answer


part = Part2()

part.add_result(900, """
forward 5
down 5
forward 8
up 3
down 8
forward 2
""")

part.add_result(1620141160)
