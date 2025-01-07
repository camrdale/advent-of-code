from pathlib import Path
import re
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
        """Retrieve any additional params that were passed to aoc.runner.Part.add_result"""
        return self.additional_params

    def get_input(self) -> list[str]:
        """Get the input lines."""
        return [line.strip() for line in self.input]

    def get_two_part_input(self) -> tuple[list[str], list[str]]:
        """Get input that is two parts, separated by a blank line."""
        input = self.get_input()
        split_at = input.index('')
        return input[:split_at], input[split_at+1:]

    def get_split_input(self) -> list[list[str]]:
        """Get the input lines split by whitespace."""
        return [line.split() for line in self.get_input()]
    
    def get_input_coords(self) -> list[Coordinate]:
        """Get the input converted into Coordinates."""
        return [
            Coordinate(*map(int, line.split(',')))
            for line in self.get_input()
            if len(line) > 0]

    def get_parsed_input(self, regex: re.Pattern[str]) -> list[tuple[str, ...]]:
        """Get the input lines parsed by a regex."""
        results: list[tuple[str, ...]] = []
        for line in self.get_input():
            match = regex.match(line)
            if not match:
                print('ERROR failed to match input regex for line:', line)
                continue
            results.append(match.groups())
        return results

    def get_multipart_parsed_input(
            self,
            *regexes: re.Pattern[str]
            ) -> list[dict[re.Pattern[str], tuple[str, ...]]]:
        """Get the input that is multiple parts, each part having lines that match regexes.
        
        The input parts are expected to be separated by a blank line.

        Returns a list with a dictionary for each part found. The dictionary
        keys are the regexes that were found, regexes that were not found will
        not appear in the dictionary. The value is the matching groups that
        were found for that regex. If a regex matches multiple times, only the
        last match will be included in the dictionary.
        """
        results: list[dict[re.Pattern[str], tuple[str, ...]]] = []
        result: dict[re.Pattern[str], tuple[str, ...]] = {}
        for line in self.get_input():
            if line == '':
                results.append(result)
                result = {}
                continue
            for regex in regexes:
                match = regex.match(line)
                if match:
                    result[regex] = match.groups()
        results.append(result)
        return results
