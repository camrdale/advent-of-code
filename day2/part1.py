from pathlib import Path

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import Report, Visualizer


class Part1(Part):
    def __init__(self, visualize: bool = True):
        super().__init__()
        self.visualize = visualize

    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        visualizer: Visualizer | None = None
        if self.visualize:
            visualizer = Visualizer()

        reports: list[Report] = []
        for line in input:
            reports.append(Report(list(map(int, line.split()))))

        if visualizer is not None:
            visualizer.draw_reports(
                'The initial reports (green = gradual increase, red = increase too fast, blue = decrease)',
                reports, 5)

        normalized = [report.normalize() for report in reports]

        if visualizer is not None:
            visualizer.animate_normalization(
                'For simplicity, normalize all reports to be increasing (reverse decreasing reports)',
                reports, normalized, 5)

            visualizer.draw_reports('', normalized, 1)

            visualizer.fade_out_unsafe(
                'Remove any reports that are unsafe (red or blue)',
                normalized, 5)

        num_safe_reports = sum(1 for report in normalized if report.safe())

        if visualizer is not None:
            visualizer.draw_reports(
                '{} safe reports remain'.format(num_safe_reports),
                normalized, 3, safe_only=True)

        log(RESULT, 'Number of safe reports:', num_safe_reports)

        if visualizer is not None:
            visualizer.finalize()
            visualizer.outputMovie(Path(__file__).parent.resolve() / 'part1.mp4')

        return num_safe_reports


part = Part1(visualize=False)

part.add_result(2, """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""")

part.add_result(483)
