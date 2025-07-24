from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import Report


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        reports: list[Report] = []
        for line in input:
            reports.append(Report(list(map(int, line.split()))))

        normalized = [report.normalize() for report in reports]

        num_safe_reports = sum(1 for report in normalized if report.safe())

        log(RESULT, 'Number of safe reports:', num_safe_reports)
        return num_safe_reports


part = Part1()

part.add_result(2, """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""")

part.add_result(483)
