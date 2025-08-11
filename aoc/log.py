from collections.abc import Iterable
from typing import Any, TypeVar, Self
from types import TracebackType

from tqdm import tqdm

# Log levels

# Don't log anything
NONE = -2
# Don't log anything, but instead create progress bars
PROGRESS = -1
# Only the final result of a part can use this level
RESULT = 0
# Useful information, such as is shown in the AoC example output
INFO = 1
# Debugging information, more verbose
DEBUG = 2
# Debugging information for INTCODE operations
INTCODE = 3
# The most verbose
VERBOSE = 4

# Default log level is to only print the result line.
log_level = RESULT


def set_log_level(new_level: int) -> None:
    global log_level
    log_level = new_level


def get_log_level() -> int:
    return log_level


def log(level: int, *args: Any) -> None:
    """Print a log message if the log level allows it."""
    if level <= log_level:
        if len(args) == 1 and callable(args[0]):
            print(args[0]())
        else:
            print(*args)


T = TypeVar('T')
next_progressbar_position = 0


def progress_bar(iter: Iterable[T], desc: str|None = None) -> Iterable[T]:
    global next_progressbar_position
    progress_bar_enabled = get_log_level() == PROGRESS
    if progress_bar_enabled:
        position = next_progressbar_position
        next_progressbar_position += 1
        iter = tqdm(iter, position=position, leave=None, desc=desc)
    for x in iter:
        yield x
    if progress_bar_enabled:
        next_progressbar_position -= 1


class ProgressBar:
    def __init__(self, estimated_iterations: int, desc: str|None = None):
        self.estimated_iterations = estimated_iterations
        self.desc = desc

    def __enter__(self) -> Self:
        global next_progressbar_position
        progress_bar_disabled = get_log_level() != PROGRESS
        position = next_progressbar_position
        next_progressbar_position += 1
        self.tqdm = tqdm(
            total=self.estimated_iterations, 
            disable=progress_bar_disabled, 
            position=position, 
            leave=None, 
            desc=self.desc)
        return self

    def __exit__(self, exc_type: type[BaseException], exc_value: BaseException, traceback: TracebackType):
        self.tqdm.close()
        global next_progressbar_position
        next_progressbar_position -= 1

    def update(self, n: int = 1):
        self.tqdm.update(n=n)
