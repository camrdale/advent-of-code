#!/usr/bin/python

from pathlib import Path

from shared import Report, Visualizer

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'

visualizer = Visualizer()

reports: list[Report] = []
with INPUT_FILE.open() as ifp:
    for line in ifp.readlines():
        reports.append(Report(list(map(int, line.split()))))

visualizer.draw_reports(
    'The initial reports (green = gradual increase, red = increase too fast, blue = decrease)',
    reports, 5)

normalized = [report.normalize() for report in reports]

visualizer.animate_normalization(
    'For simplicity, normalize all reports to be increasing (reverse decreasing reports)',
    reports, normalized, 5)

visualizer.draw_reports('', normalized, 1)

visualizer.fade_out_unsafe(
    'Remove any reports that are unsafe (red or blue)',
    normalized, 5)

num_safe_reports = sum(1 for report in normalized if report.safe())

visualizer.draw_reports(
    '{} safe reports remain'.format(num_safe_reports),
    normalized, 3, safe_only=True)

print('Number of safe reports:', num_safe_reports)

visualizer.finalize()

visualizer.outputMovie(Path(__file__).parent.resolve() / 'part1.mp4')
