from pathlib import Path
from typing import Any

from .map import Coordinate


class InputParser:
    """A parser for reading and parsing an AoC input file or test input."""

    @classmethod
    def for_test_data(cls, test_data: str, *args: Any) -> 'InputParser':
        input = test_data.split('\n')
        # Remove empty lines from the start and end of the test data.
        while input[0] == '':
            del input[0]
        while input[-1] == '':
            del input[-1]
        return InputParser(input, *args)

    @classmethod
    def for_file_input(cls, path: Path, *args: Any) -> 'InputParser':
        with path.open() as ifp:
            return InputParser(ifp.readlines(), *args)

    def __init__(self, input: list[str], *args: Any):
        self.input = input
        self.additional_params = args

    def get_additional_params(self) -> tuple[Any, ...]:
        return self.additional_params

    def get_input(self) -> list[str]:
        return [line.strip() for line in self.input]
    
    def get_input_coords(self) -> list[Coordinate]:
        return [
            Coordinate(*map(int, line.strip().split(',')))
            for line in self.get_input()
            if len(line.strip()) > 0]
