#!/usr/bin/python

from collections import defaultdict
import datetime
import importlib
from pathlib import Path
import re
import sys

from aoc.log import set_log_level, RESULT, INFO
from aoc.runner import Part

DAY_DIR = re.compile(r'^day([0-9]*)$')
PART_FILE = re.compile(r'part([0-9]*).py')


def run_part(day: int, part_num: int) -> bool:
    part_module = importlib.import_module(f'day{day}.part{part_num}')
    part: Part = part_module.part
    return part.run_part(day, part_num)


def find_parts(day_dir: Path) -> list[int]:
    parts: list[int] = []
    for part_file in day_dir.glob('part*.py'):
        part_match = PART_FILE.match(part_file.name)
        if not part_match:
            continue
        parts.append(int(part_match.group(1)))
    return parts


def run_day(day: int, latest_only: bool=False):
    """Run all parts (by default) for a specific day."""
    set_log_level(RESULT)  # only log the final result for each input
    day_dir = Path(sys.argv[0]).parent.resolve() / f'day{day}'
    if not day_dir.is_dir():
        print(f'ERROR Failed to find directory for: day{day}')
        return
    
    parts: list[int] = find_parts(day_dir)
    
    if len(parts) == 0:
        print(f'ERROR Failed to find any part files in directory for: day{day}')
        return

    parts.sort()
    if latest_only:
        run_part(day, parts[-1])
    else:
        for part in parts:
            run_part(day, part)


def run_today():
    """Run the latest part created for today."""
    run_day(datetime.date.today().day, latest_only=True)


def run_all():
    """Run both parts for every day so far."""
    set_log_level(-1)  # don't log anything while running each part
    parts: list[tuple[int, int]] = []
    for day_dir in Path(sys.argv[0]).parent.resolve().glob('day*'):
        if not day_dir.is_dir():
            continue
        day_match = DAY_DIR.match(day_dir.name)
        if not day_match:
            continue

        day = int(day_match.group(1))
        parts.extend((day, part) for part in find_parts(day_dir))

    parts.sort()
    fails = 0
    fail_parts: dict[int, int] = defaultdict(int)
    for day, part in parts:
        if not run_part(day, part):
            fails += 1
            fail_parts[part] += 1

    print(f'Ran {len(parts)} parts, failed on {fails} ({fail_parts[1]} on part 1s, {fail_parts[2]} on part 2s)')


if __name__ == '__main__':
    run_today()
    # run_day(17)
    # run_all()
    set_log_level(INFO)
    # run_part(21, 2)
