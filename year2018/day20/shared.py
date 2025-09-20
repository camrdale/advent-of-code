from typing import Self

from aoc.map import UnknownMap, Coordinate, UP, DOWN, LEFT, RIGHT


PATH = u'\u2588'


class Regex:
    def __init__(self, children: list[RegexText | RegexBranch]) -> None:
        self.children: list[RegexText | RegexBranch] = children

    @classmethod
    def parse(cls, input: str) -> tuple[Self, int]:
        children: list[RegexText | RegexBranch] = []
        i = 0
        while i < len(input) and input[i] not in '|)':
            if input[i] == '(':
                child, l = RegexBranch.parse(input[i:])
            else:
                child, l = RegexText.parse(input[i:])
            children.append(child)
            i += l
        return cls(children), i

    def __repr__(self) -> str:
        return ''.join(repr(child) for child in self.children)
    
    def follow(self, starting_locations: set[Coordinate]) -> tuple[set[Coordinate], set[Coordinate]]:
        found_locations: set[Coordinate] = set()
        ending_locations = starting_locations
        for child in self.children:
            child_locations, ending_locations = child.follow(ending_locations)
            found_locations.update(child_locations)
        return found_locations, ending_locations


DIRECTIONS = {'N': UP, 'S': DOWN, 'E': RIGHT, 'W': LEFT}


class RegexText:
    def __init__(self, text: str) -> None:
        self.text = text

    @classmethod
    def parse(cls, input: str) -> tuple[Self, int]:
        text = ''
        i = 0
        while i < len(input) and input[i] in DIRECTIONS:
            text += input[i]
            i += 1
        return cls(text), i

    def __repr__(self) -> str:
        return self.text

    def follow(self, starting_locations: set[Coordinate]) -> tuple[set[Coordinate], set[Coordinate]]:
        ending_locations: set[Coordinate] = set()
        found_locations: set[Coordinate] = set()

        for location in starting_locations:
            for c in self.text:
                location = location.add(DIRECTIONS[c])
                found_locations.add(location)
                location = location.add(DIRECTIONS[c])
                found_locations.add(location)
            ending_locations.add(location)

        return found_locations, ending_locations


class RegexBranch:
    def __init__(self, branches: list[Regex]) -> None:
        self.branches: list[Regex] = branches

    @classmethod
    def parse(cls, input: str) -> tuple[Self, int]:
        assert input[0] == '(', input
        branches: list[Regex] = []
        i = 1
        while input[i - 1] != ')':
            branch, l = Regex.parse(input[i:])
            branches.append(branch)
            i += l + 1
        return cls(branches), i

    def __repr__(self) -> str:
        return f'({"|".join(repr(branch) for branch in self.branches)})'

    def follow(self, starting_locations: set[Coordinate]) -> tuple[set[Coordinate], set[Coordinate]]:
        ending_locations: set[Coordinate] = set()
        found_locations: set[Coordinate] = set()

        for branch in self.branches:
            child_locations, child_endings = branch.follow(starting_locations)
            found_locations.update(child_locations)
            ending_locations.update(child_endings)

        return found_locations, ending_locations


class FacilityMap(UnknownMap):
    def __init__(self, regex: Regex):
        super().__init__(PATH)
        self.add_feature(PATH, Coordinate(0, 0))
        locations, _ = regex.follow({Coordinate(0, 0)})
        for location in locations:
            self.add_feature(PATH, location)

    def valid(self, coordinate: Coordinate) -> bool:
        """Check if a Coordinate is valid for this map."""
        return coordinate in self.features[PATH]

    def rooms(self) -> dict[Coordinate, int]:
        """Return each room location, and the number of doors needed to get to it by the shortest path."""
        visited, _ = self.shortest_paths(Coordinate(0, 0), Coordinate(0, 0))
        return {location: distance // 2 for location, distance in visited.items() if distance % 2 == 0}
