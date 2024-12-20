from typing import Any

# Log levels

# Only the final result of a part can use this level
RESULT = 0
# Useful information, such as is shown in the AoC example output
INFO = 1
# Debugging information, more verbose
DEBUG = 2
# The most verbose
VERBOSE = 3

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
        print(*args)
