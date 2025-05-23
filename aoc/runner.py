from abc import ABC, abstractmethod
from pathlib import Path
import sys
import time
from typing import Any

from aoc.input import InputParser
from aoc import log


class Part(ABC):
    """One part of a problem for a single day."""
    def __init__(self):
        self.test_data_and_results: list[tuple[str | None, Any, bool|None]] = []
        self.additional_params: list[tuple[Any, ...]] = []

    @abstractmethod
    def run(self, parser: InputParser) -> Any:
        """Override this to run the input data, returning the result."""
        pass

    def add_result(self, result: Any, test_data: str | None=None, *additional_params: Any, include_progress: bool|None = None):
        """Add an expected result of running the part, either for test_data input, or for the input file."""
        self.test_data_and_results.append((test_data, result, include_progress))
        self.additional_params.append(additional_params)

    def run_part(self, year: int, day: int, part_num: int, subdirectory: Path | None = None) -> bool:
        """Run all the input data for this part, returning whether it matched the expected."""
        success = True
        i = 0
        end = start = 0.0
        for test_data, expected_result, include_progress in self.test_data_and_results:
            i += 1
            final_data = i == len(self.test_data_and_results)
            if final_data and not success:
                break

            log.log(log.RESULT, f'Running year{year}, day{day}, part{part_num}', 'final data' if final_data else f'test data {i}')

            if test_data is not None:
                parser = InputParser.for_string_input(test_data, *self.additional_params[i-1])
            else:
                base_path = Path(sys.argv[0]).parent.resolve() / f'year{year}' / f'day{day}'
                if subdirectory is not None:
                    base_path = subdirectory.parent.resolve()
                parser = InputParser.for_file_input(
                    base_path / 'input.txt',
                    *self.additional_params[i-1])

            original_log_level: int|None = None
            if not final_data and log.get_log_level() == log.PROGRESS and not include_progress:
                original_log_level = log.get_log_level()
                log.set_log_level(log.NONE)

            try:
                start = time.time()
                result = self.run(parser)
                end = time.time()

            finally:
                if original_log_level is not None:
                    log.set_log_level(original_log_level)

            if expected_result != result:
                print(f'FAIL on year{year}, day{day} part{part_num}', 'final data' if final_data else f'test data {i}')
                if test_data is not None:
                    print(test_data)
                print(f'expected {expected_result}, but got {result}')
                success = False

        log.log(log.RESULT, f'year{year}, day{day}, part{part_num} last run took {end-start:.3f} seconds')
        # if end-start >= 5.0:
        #     print(f'year{year}, day{day}, part{part_num} last run took {end-start:.3f} seconds')

        return success
