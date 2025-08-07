import collections
import functools
import re


PROGRAM = re.compile(r'([a-z]*) \(([0-9]*)\)(?: -> )?([a-z, ]*)?')


class Program:
    def __init__(self) -> None:
        self.supported: list[Program] = []

    def initialize(self, name: str, weight: int) -> None:
        self.name = name
        self.weight = weight
    
    def add_supported(self, program: Program) -> None:
        self.supported.append(program)

    @functools.cached_property
    def tower_weight(self) -> int:
        return self.weight + sum(program.tower_weight for program in self.supported)

    @classmethod
    def create_tower(cls, input: list[str]) -> Program:
        """Creates a tower of programs and returns the program at the base."""
        bases: set[str] = set()
        supporteds: set[str] = set()
        programs: dict[str, Program] = collections.defaultdict(Program)
        for line in input:
            match = PROGRAM.match(line)
            assert match is not None, line
            program = programs[match.group(1)]
            program.initialize(match.group(1), int(match.group(2)))
            bases.add(program.name)
            if match.group(3):
                for supported in match.group(3).split(', '):
                    program.add_supported(programs[supported])
                    supporteds.add(supported)

        bottom = bases - supporteds
        assert len(bottom) == 1, bottom
        return programs[next(iter(bottom))]

    def __repr__(self) -> str:
        return f'Program({self.name}, {self.weight}, [{",".join(supported.name for supported in self.supported)}])'
