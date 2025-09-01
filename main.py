#!/usr/bin/python

from collections import defaultdict
import datetime
import importlib
from pathlib import Path
import re
import sys
import time

from aoc import log
from aoc.runner import Part

YEAR_DIR = re.compile(r'^year([0-9]*)$')
DAY_DIR = re.compile(r'^day([0-9]*)$')
PART_FILE = re.compile(r'part([0-9]*).py')


def run_part(year: int, day: int, part_num: int) -> bool:
    part_module = importlib.import_module(f'year{year}.day{day}.part{part_num}')
    part: Part = part_module.part
    return part.run_part(year, day, part_num)


def find_parts(day_dir: Path) -> list[int]:
    parts: list[int] = []
    for part_file in day_dir.glob('part*.py'):
        part_match = PART_FILE.match(part_file.name)
        if not part_match:
            continue
        parts.append(int(part_match.group(1)))
    return parts


def run_day(year: int, day: int, latest_only: bool=False):
    """Run all parts (by default) for a specific day."""
    log.set_log_level(log.RESULT)  # only log the final result for each input
    day_dir = Path(sys.argv[0]).parent.resolve() / f'year{year}' / f'day{day}'
    if not day_dir.is_dir():
        print(f'ERROR Failed to find directory for: day{day}')
        return
    
    parts: list[int] = find_parts(day_dir)
    
    if len(parts) == 0:
        print(f'ERROR Failed to find any part files in directory for: day{day}')
        return

    parts.sort()
    if latest_only:
        run_part(year, day, parts[-1])
    else:
        for part in parts:
            run_part(year, day, part)


def run_today(year: int|None = None):
    """Run the latest part created for today."""
    if year is None:
        year = datetime.date.today().year
    run_day(year, datetime.date.today().day, latest_only=True)


def run_all(only_year: int|None = None):
    """Run both parts for every day so far."""
    log.set_log_level(log.PROGRESS)  # only print progress bars while running each part
    parts: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for year_dir in Path(sys.argv[0]).parent.resolve().glob('year*'):
        if not year_dir.is_dir():
            continue
        year_match = YEAR_DIR.match(year_dir.name)
        if not year_match:
            continue

        year = int(year_match.group(1))
        if only_year is not None and year != only_year:
            continue

        for day_dir in year_dir.glob('day*'):
            if not day_dir.is_dir():
                continue
            day_match = DAY_DIR.match(day_dir.name)
            if not day_match:
                continue

            day = int(day_match.group(1))
            parts[year].extend((day, part) for part in find_parts(day_dir))
        parts[year].sort()

    total_parts = 0
    fails = 0
    fail_parts: dict[int, int] = defaultdict(int)
    start = time.time()
    years = sorted(parts)
    if only_year is None:
        years = log.progress_bar(years, desc='all years')
    for year in years:
        for day, part in log.progress_bar(parts[year], desc=f'year {year}'):
            total_parts += 1
            if not run_part(year, day, part):
                fails += 1
                fail_parts[part] += 1

    end = time.time()
    print(f'Ran {total_parts} parts in {end-start:.3f} seconds, failed on {fails} ({fail_parts[1]} on part 1s, {fail_parts[2]} on part 2s)')


if __name__ == '__main__':
    run_today(year=2018)
    # run_day(2018, 1)
    # run_all(only_year=2018)
    log.set_log_level(log.INFO)
    # run_part(2018, 2, 2)
