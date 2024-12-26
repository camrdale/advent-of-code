from abc import ABC, abstractmethod
from pathlib import Path
import sys
import time
from typing import Any

from aoc.input import InputParser


class Part(ABC):
    """One part of a problem for a single day."""
    def __init__(self):
        self.test_data_and_results: list[tuple[str, Any]] = []
        self.final_result = None
        self.test_data_additional_params: list[tuple[Any, ...]] = []
        self.additional_params: tuple[Any, ...] = tuple()

    @abstractmethod
    def run(self, parser: InputParser) -> Any:
        """Override this to run the input data, returning the result."""
        pass

    def add_result(self, result: Any, test_data: str | None=None, *additional_params: Any):
        """Add an expected result of running the part, either for test_data input, or for the input file."""
        if test_data is not None:
            self.test_data_and_results.append((test_data, result))
            self.test_data_additional_params.append(additional_params)
        else:
            self.final_result = result
            self.additional_params = additional_params

    def run_part(self, year: int, day: int, part_num: int, subdirectory: Path | None = None) -> bool:
        """Run all the input data for this part, returning whether it matched the expected."""
        success = True
        i = 0
        for test_data, expected_result in self.test_data_and_results:
            i += 1
            print(f'Running year{year}, day{day}, part{part_num} test data {i}')

            parser = InputParser.for_test_data(test_data, *self.test_data_additional_params[i-1])
            result = self.run(parser)

            if expected_result != result:
                print(f'FAIL on year{year}, day{day} part{part_num} test data\n{test_data}\nexpected {expected_result}, but got {result}')
                success = False

        if not success:
            return success

        print(f'Running year{year}, day{day}, part{part_num} input file')

        base_path = Path(sys.argv[0]).parent.resolve() / f'year{year}' / f'day{day}'
        if subdirectory is not None:
            base_path = subdirectory.parent.resolve()
        parser = InputParser.for_file_input(
            base_path / 'input.txt',
            *self.additional_params)
        start = time.time()
        result = self.run(parser)
        end = time.time()

        if self.final_result is not None and self.final_result != result:
            print(f'FAIL on year{year}, day{day}, part{part_num} input data, expected {self.final_result}, but got {result}')

        print(f'year{year}, day{day}, part{part_num} took {end-start:.3f} seconds to run')

        return self.final_result == result
